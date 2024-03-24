#include <Arduino.h>



class AuthData 
{
    private:
        struct siteCredentials {
            String siteUsername;
            byte *sitePass;
        } thisCredential;

    public:
        void setSiteUser(String sUser);
        void setSitePassword(const char *sPass);
        String getSiteUser();
        byte* getSitePass();


};