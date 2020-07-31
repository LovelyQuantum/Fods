#include <stdio.h>
#include <string.h>
#include "public.h"
#include "Alarm.h"


#ifdef _WIN32
#elif defined(__linux__) || defined(__APPLE__)
#include   <unistd.h> 
#endif


void CALLBACK MessageCallback(LONG lCommand, NET_DVR_ALARMER *pAlarmer, char *pAlarmInfo, DWORD dwBufLen, void* pUser)
{
	int i;
	NET_DVR_ALARMINFO_V30 struAlarmInfo;
	memcpy(&struAlarmInfo, pAlarmInfo, sizeof(NET_DVR_ALARMINFO_V30));
	//printf("lCommand is %d, alarm type is %d\n", lCommand, struAlarmInfo.dwAlarmType);
	switch(lCommand) 
	{       
	case COMM_ALARM_V30:
		{
			switch (struAlarmInfo.dwAlarmType)
			{
			case 3:
				for (i=0; i<16; i++)   //#define MAX_CHANNUM   16
				{
					if (struAlarmInfo.byChannel[i] == 1)
					{
						printf("Motion detection %d\n", i+1);
					}
				}       
				break;
			default:
				break;
			}
		}
		break;
	default:
		break;
	}
}


//Alarm Test
int Demo_Alarm()
{
	if (Demo_AlarmFortify() == HPR_ERROR)
	{
		return HPR_ERROR;
	}

    return HPR_OK;
}

//Alarm listen
int Demo_AlarmListen()
{
    BOOL iRet;

    //Init
    iRet = NET_DVR_Init();
    if (!iRet)
    {
        printf("   pyd---Alarm. NET_DVR_Init fail!\n");
        return HPR_ERROR;
    }
	//open
	int iHandle = NET_DVR_StartListen_V30("0.0.0.0", 7200, MessageCallback, NULL);
	if (iHandle < 0)
	{
		printf("   pyd---Alarm. NET_DVR_StartListen_V30 fail!%d\n", NET_DVR_GetLastError());
		return HPR_ERROR;
	}
    //close
    iRet = NET_DVR_StopListen_V30(iHandle);
    if (!iRet)
    {
        printf("   pyd---Alarm. NET_DVR_StopListen fail!%d\n", NET_DVR_GetLastError());
        return HPR_ERROR;
    }

    //clean up
    NET_DVR_Cleanup();

    return HPR_ERROR;
}

// Fortify
int Demo_AlarmFortify()
{
	    LONG lUserID;
        NET_DVR_USER_LOGIN_INFO struLoginInfo = {0};
        NET_DVR_DEVICEINFO_V40 struDeviceInfoV40 = {0};
        struLoginInfo.bUseAsynLogin = false;

        struLoginInfo.wPort = 8000;
        memcpy(struLoginInfo.sDeviceAddress, "192.168.103.9", NET_DVR_DEV_ADDRESS_MAX_LEN);
        memcpy(struLoginInfo.sUserName, "admin", NAME_LEN);
        memcpy(struLoginInfo.sPassword, "yk7012410", NAME_LEN);

        lUserID = NET_DVR_Login_V40(&struLoginInfo, &struDeviceInfoV40);
	if (lUserID < 0)
	{
		printf("Login error, %d\n", NET_DVR_GetLastError());
		NET_DVR_Cleanup();
		return HPR_ERROR;
	}
    NET_DVR_SetAlarmOut(lUserID, 0, 1);
    sleep(10);
    NET_DVR_SetAlarmOut(lUserID, 0, 0);
	NET_DVR_Logout_V30(lUserID);
	NET_DVR_Cleanup();
	return HPR_OK;
}
