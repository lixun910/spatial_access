import re
import itertools as it
import usaddress as add


def fix_duplicate_addresses(df,key='ClusterID',target='Address_SVC'):
    '''
    '''

    sorter = df[target].str.len().sort_values(ascending=False).index
    df = df.reindex(sorter)

    #key = [key]

    minimized_df = df[[key,target]].drop_duplicates().dropna().loc[:,[key,target]]
    #print(minimized_df)
    unique_keys = list(df[key].unique())

    for uKey in unique_keys:
        local_df = minimized_df[minimized_df[key] == uKey]
        if len(local_df) > 1:
            local_df2 = iter_df(local_df.copy().drop_duplicates().reset_index(drop=True),target)
            if local_df2[key].max() == '134': # is next
                print(local_df)
                print(local_df2)
                print('---------------------------------------------------------------')

    # Need to merge changes back into the original df


    return df


def iter_df(df,field):
    '''
    '''

    df = df.reset_index(drop=True)

    matches, unmatches = [], []

    for idx1, idx2 in it.combinations(range(len(df)),2):
        string1 = df.loc[idx1,field]
        string2 = df.loc[idx2,field]
        result, fix = pairwise_comparison(string1,string2)
        if result:
            matches.append(tuple((idx1,idx2)))
            if fix:
                df = update_df(df,field,idx1,idx2)
        else:
            unmatches.append(tuple((idx1,idx2)))

    return df


def update_df(df,field,idx1,idx2):
    '''
    '''

    min_idx = min(idx1,idx2)
    max_idx = max(idx1,idx2)

    target_string = df.loc[min_idx,field]
    df.loc[max_idx,field] = target_string

    return df


def pairwise_comparison(string1,string2):
    '''
    Parses two strings into usaddress dictionaries, then compares the
    dictionaries to assess whether the addresses are the same. Returns True if
    so and False if not.
    '''

    s1_dicto = add.tag(string1)[0]
    s2_dicto = add.tag(string2)[0]

    same = True
    fix = []

    if 'StreetNamePostType' not in s1_dicto.keys() and 'StreetNamePostType' in \
        s2_dicto.keys():
        fix.append('StreetNamePostType')

    for key, value1 in s1_dicto.items():
        '''
        What if the key from the first dicto isn't in the second dicto?
        Should the address number be held to a different standard?
        What about the city, state, and zip? Should those be concatenated and considered, too?

        '''
        if key == 'StreetNamePostType':
            if key in s2_dicto.keys():
                if value1 != s2_dicto[key]:
                    fix.append(key)
            else:
                fix.append(key)
            continue
        if key in s2_dicto.keys():
            value2 = s2_dicto[key]
        else:
            fix.append(key)
            continue
        if key == 'AddressNumber':
            if value1 == value2:
                continue
            else:
                same = False
                break
        elif value1 == value2:
            continue
        elif is_substring(value1,value2):
            fix.append(key)
            continue
        else:
            same = False
            break

    if len(s1_dicto) == 1 and not is_substring(string1,string2):
        same = False
    elif len(s2_dicto) == 1 and not is_substring(string2,string1):
        same = False

    return same, fix


def ns(string):
    '''
    '''

    ns_string = string.replace(' ','')

    return ns_string


def is_substring(string1,string2):
    '''
    '''

    if not re.findall(string1,string2):
        if not re.findall(string2,string1):
            if not re.findall(ns(string1),ns(string2)):
                if not re.findall(ns(string2),ns(string1)):
                    return False

    return True


# DEPRECATED FUNCTION
def compare_addresses(df,address_field):
    '''
    Takes a dataframe and the name of an address field, then does pairwise
    comparisons on the strings in the field. Returns True if they are all the
    same and False if at least one is different.
    '''

    same = True

    for string1, string2 in it.combinations(df[field],2):
        same = pairwise_comparison(string1,string2)
        if not same:
            break

    return same
