#include "filesystem.h"
#include "Arduino.h"
#include "Crypto.h"



void AuthData::setSiteUser(String suser){
    thisCredential.siteUsername = suser;
}

void AuthData::setSitePassword(const char *spass){
    SHA256 hasher;
    hasher.doUpdate(spass);
    byte hash[SHA256_SIZE];
    hasher.doFinal(hash);
    thisCredential.sitePass = hash;
};

String AuthData::getSiteUser(){
    return thisCredential.siteUsername;
};

byte* AuthData::getSitePass(){
    return thisCredential.sitePass;
};