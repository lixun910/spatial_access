import re
import UTILS as u
import numpy as np
import pandas as pd
import COMPARE_ADDRESSES as ca


LINK = '../../../rcc-uchicago/PCNO/CSV/chicago/2018-07-03_link_agencies_output.csv'
MAP1B = '../../../rcc-uchicago/PCNO/CSV/chicago/maps/map1b.csv'
SVC = '../../../rcc-uchicago/PCNO/CSV/chicago/service_agencies.csv'
GEO = '../../../rcc-uchicago/PCNO/CSV/chicago/map2_geocoding.csv'
GEO2 = '../../../rcc-uchicago/PCNO/CSV/chicago/map2_geocoding_version2.csv'
DOLLARS_DIVIDED = '../../../rcc-uchicago/PCNO/CSV/chicago/dollars_divided.csv'

THRESH = 0.34


def read_linker():
    '''
    Reads in the linked agencies file, retains matches >= the THRESH level, then
    drops two columns. Returns a dataframe.
    '''

    df = pd.read_csv(LINK,converters={'ClusterID':str})

    df = df[df['LinkScore'] >= THRESH]

    df = df.drop(['LinkScore','SourceFile'],axis=1)

    return df


def linker():
    '''
    Reads in the linker file (to link HQ agencies to service agencies). Merges a
    copy of itself on cluster ID, then eliminates records that match on vendor
    ID (to produce only matches that have different vendor IDs). Returns a
    dataframe.
    '''

    link = read_linker()
    link1 = link.rename(columns={'VendorName':'VendorName_LINK1'},index=str)
    link2 = u.rename_cols(link,['VendorName','CSDS_Vendor_ID'],'_LINK2')

    df = link1.merge(link2,how='left')
    df = df[df['CSDS_Vendor_ID'] != df['CSDS_Vendor_ID_LINK2']].reset_index(drop=True)

    return df


def insert_marginal_hq(df):
    '''
    '''

    list_of_dictos = []

    for row in df.itertuples(index=False):
        if row.Address_SVC is not np.NaN:
            if row.Address != row.Address_SVC:
                dicto = row._asdict()
                list_of_dictos.append(dicto)

    for dicto in list_of_dictos:
        dicto['Address_SVC'] = dicto['Address']
        dicto['City_SVC'] = dicto['City']
        dicto['State_SVC'] = dicto['State']
        dicto['ZipCode_SVC'] = dicto['ZipCode']
        dicto['CSDS_Org_ID_SVC'] = np.NaN

    appender = pd.DataFrame(list_of_dictos)

    df_aug = pd.concat([df,appender])
    df_aug = df_aug.drop_duplicates()

    return df_aug


def merger():
    '''
    '''

    link = linker()
    hq = read_hq()[['CSDS_Vendor_ID','VendorName','Agency_Summed_Amount','Address',
                    'City','State','ZipCode','Longitude','Latitude']].drop_duplicates()
    svc = read_svc()

    merged = hq.merge(link,how='left').merge(svc,how='left')
    df_aug = insert_marginal_hq(merged)

    mega_df = pd.concat([merged,df_aug])
    mega_df = mega_df.drop_duplicates(subset=['CSDS_Vendor_ID','Address_SVC']).reset_index(drop=True)

    return mega_df



def dollars_per_location(merged):
    '''
    Reads in the service agencies and the HQ agencies, then links them (using
    the linker dataframe). Calculates the number of dollars per location.
    Returns a dataframe.
    '''



    cols = ['Address','City','State','ZipCode']

    for col in cols:
        merged[col + '_SVC'] = merged[col + '_SVC'].combine_first(merged[col])

    coords = ['Longitude','Latitude']
    for col in coords:
        merged[col + '_SVC'] = merged.apply(lambda x: x[col] if
                                        (x['Address'] == x['Address_SVC']) and
                                        (x['City'] == x['City_SVC']) and
                                        (x['State'] == x['State_SVC'])
                                        else np.NaN, axis=1)

    # Need to account for HQ addresses with different zips
    merged2 = merged.sort_values(['CSDS_Vendor_ID','Address_SVC','City_SVC',
                                  'State_SVC','ZipCode_SVC'],ascending=True)

    merged2 = merged2.drop_duplicates(subset=['CSDS_Vendor_ID','Address','City',
                                              'State','Address_SVC','City_SVC',
                                              'State_SVC'],keep='first')

    merged2['HQ_Flag'] = merged2.apply(lambda x: 1 if
                                    (x['Address'] == x['Address_SVC']) and
                                    (x['City'] == x['City_SVC']) and
                                    (x['State'] == x['State_SVC']) else 0,
                                    axis=1)

    counts = count_svc_addr(merged2)
    numbered = merged2.merge(counts,how='left')

    dollars_div = numbered.assign(Dollars_Per_Location=numbered['Agency_Summed_Amount']\
                           / numbered['Num_Svc_Locations'])

    return dollars_div.drop_duplicates().reset_index(drop=True)


def read_hq():
    '''
    Reads in the contracts with HQ addresses; converts the zip codes to strings.
    Adds up the contract amounts per agency. Returns a dataframe.
    '''

    df = pd.read_csv(MAP1B,converters={'Zip':str})

    df = df.rename(columns={'Zip':'ZipCode'},index=str)

    agg_amounts = agg_funds(df)
    merged = df.merge(agg_amounts)

    return merged


def read_svc():
    '''
    Reads in the service agency addresses. Calls the COMPARE_ADDRESSES module to
    merge duplicate addresses per agency. Counts the number of service addresses
    per organization. Returns a dataframe.
    '''

    print('\nReading in service agencies')

    df = pd.read_csv(SVC,converters={'ZipCode':str})
    df = u.rename_cols(df,[x for x in df.columns if x != 'CSDS_Svc_ID'],'_SVC')
    df = df.rename(columns={'CSDS_Svc_ID':'CSDS_Vendor_ID_LINK2'},index=str)

    key = 'CSDS_Vendor_ID_LINK2'
    target = 'Address_SVC'
    fixed_addresses = ca.fix_duplicate_addresses(df,key,target)
    fixed_addresses = fixed_addresses.drop_duplicates(subset=[key,target])

    '''
    counts = count_svc_addr(fixed_addresses)
    merged = fixed_addresses.merge(counts)

    return merged.reset_index(drop=True)
    '''

    return fixed_addresses


def agg_funds(hq):
    '''
    Adds up the contract amounts per HQ agency. Returns a dataframe.
    '''

    agg = hq.groupby('CSDS_Vendor_ID')['Amount'].sum().reset_index()
    agg = agg.rename(columns={'Amount':'Agency_Summed_Amount'},index=str)

    return agg


def count_svc_addr(df):
    '''
    Counts the number of service addresses per agency. Returns a dataframe.
    '''

    df = df.assign(Constant=1)
    counts = df.groupby('CSDS_Vendor_ID')['Constant'].count()
    counts.name = 'Num_Svc_Locations'

    return counts.to_frame().reset_index()


def separate_satellites(df):
    '''
    The problem right now is that this is keeping HQs that have satellites and
    only excluding HQs with no satellites.

    Going to leave this alone and deal with it in the map2 script.
    '''

    keep = ['CSDS_Vendor_ID','VendorName','CSDS_Org_ID_SVC','City_SVC',
            'State_SVC','ZipCode_SVC','Longitude_SVC','Latitude_SVC',
            'Address_SVC','Dollars_Per_Location']

    satellites = df.dropna(subset=['Num_Svc_Locations'])
    satellites = satellites[satellites['Num_Svc_Locations'] > 1]
    satellites = satellites[keep]

    new_names = [re.sub('_SVC$','',x) for x in keep]
    cn = dict(zip(keep,new_names))

    satellites = satellites.rename(columns=cn,index=str)

    return satellites.reset_index(drop=True)


def needs_geocoding(df):
    '''
    Keeps only the records that have not been geocoded. Returns a dataframe.
    '''

    id = 'CSDS_Org_ID'
    lat = 'Latitude'
    lon = 'Longitude'
    address_fields = ['Address','City','State','ZipCode']

    needs_geo = df[[id,lat,lon] + [x for x in address_fields]].drop_duplicates()
    needs_geo = needs_geo[pd.isnull(needs_geo[lat])]
    needs_geo = needs_geo.drop([lat,lon],axis=1)
    needs_geo = needs_geo.dropna(subset=['CSDS_Org_ID'])

    needs_geo = needs_geo.rename(columns={'ZipCode':'Zip','CSDS_Org_ID':'ID'},index=str)

    return needs_geo.reset_index(drop=True)


if __name__ == '__main__':

    merged = merger()

    dollars_div = dollars_per_location(merged)
    dollars_div.to_csv(DOLLARS_DIVIDED,index=False)

    # This is the correct amount:  3810692646.1199999

    satellites = separate_satellites(dollars_div)

    needs_geo = needs_geocoding(satellites)
    needs_geo.to_csv(GEO2,index=False)
