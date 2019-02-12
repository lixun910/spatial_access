#pragma once

#include <unordered_map>

class userDataPoint
{
public:
    int networkNodeId;
    unsigned int loc;
    int lastMileDistance;
    userDataPoint(int networkNodeId, unsigned int loc, int lastMileDistance);
};

class userDataTract
{
public:
    int networkNodeId;
    std::vector<userDataPoint> data;
    userDataTract(int networkNodeId);
    void addPoint(userDataPoint userData);
    void print() const;
    const std::vector<userDataPoint>& retrieveDataPoints() const;
};


class userDataContainer
{
public:
    bool isSymmetric;
    std::unordered_map<int, userDataTract> data;
    std::vector<int> allNetworkNodeIds;
    std::vector<unsigned int> ids;
    std::vector<int> uniqueNetworkNodeIds;
    userDataContainer();
    void addPoint(int networkNodeId, unsigned int loc, int lastMileDistance);
    bool containsTract(int networkNodeId) const;
    const userDataTract& retrieveTract(int networkNodeId) const;
    const std::vector<unsigned  int>& retrieveAllUserDataIds() const;
    const std::vector<int>& retrieveAllNetworkNodeIds() const;
    const std::vector<int>& retrieveUniqueNetworkNodeIds() const;
    void print() const;
};
