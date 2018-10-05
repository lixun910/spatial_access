#pragma once

#include <vector>
#include <string>
#include <unordered_map>
#include <iostream>

class userDataPoint
{
public:
    int networkNodeId;
    std::string id;
    int lastMileDistance;
    userDataPoint(int networkNodeId, std::string id, int lastMileDistance);
};

userDataPoint::userDataPoint(int networkNodeId, std::string id, int lastMileDistance)
{
    this->networkNodeId = networkNodeId;
    this->id = id;
    this->lastMileDistance = lastMileDistance;
}




class userDataTract
{
public:
    int networkNodeId;
    std::vector<userDataPoint> data;
    userDataTract(int networkNodeId);
    void addPoint(userDataPoint userData);
    void print();
};

void userDataTract::print()
{
    std::cout << networkNodeId << std::endl;
    for (auto dataPoint : data)
    {
        std::cout << "(" << dataPoint.id << "," << dataPoint.lastMileDistance << ")" << std::endl;
    }
}

userDataTract::userDataTract(int networkNodeId)
{
    this->networkNodeId = networkNodeId;
}

void userDataTract::addPoint(userDataPoint userData)
{
    data.push_back(userData);
}



class userDataContainer
{
public:
    std::unordered_map<int, userDataTract> data;
    std::vector<int> allNetworkNodeIds;
    std::vector<std::string> ids;
    userDataContainer();
    void addPoint(int networkNodeId, std::string id, int lastMileDistance);
    bool containsTract(int networkNodeId);
    userDataTract retrieveTract(int networkNodeId);
    const std::vector<std::string>& retrieveAllUserDataIds();
    const std::vector<int>& retrieveAllNetworkNodeIds();
    void print();
};

const std::vector<std::string>& userDataContainer::retrieveAllUserDataIds()
{
    return this->ids;
}

void userDataContainer::print()
{
    for (auto entry : data)
    {
        entry.second.print();
    }
}

userDataContainer::userDataContainer()
{

}
bool userDataContainer::containsTract(int networkNodeId)
{
    // improve search time using set
    return data.find(networkNodeId) != data.end();
}
void userDataContainer::addPoint(int networkNodeId, std::string id, int lastMileDistance)
{
    ids.push_back(id);
    allNetworkNodeIds.push_back(networkNodeId);
    userDataPoint newDataPoint(networkNodeId, id, lastMileDistance);
    if (containsTract(networkNodeId))
    {
        data.at(networkNodeId).addPoint(newDataPoint);
    }
    else
    {
        userDataTract newUserDataTract(networkNodeId);
        newUserDataTract.addPoint(newDataPoint);
        data.insert(std::make_pair(networkNodeId, newUserDataTract));
    }
}

userDataTract userDataContainer::retrieveTract(int networkNodeId)
{
    return data.at(networkNodeId);
}

const std::vector<int>& userDataContainer::retrieveAllNetworkNodeIds()
{
    return allNetworkNodeIds;
}