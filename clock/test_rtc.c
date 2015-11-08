#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <linux/rtc.h>

int main(int argc, char *argv[])
{
	int rtc_fd;
	int ret;
	struct rtc_time rtc_tm;

	rtc_fd = open("/dev/rtc", O_RDONLY, 0);
	ret = ioctl(rtc_fd, RTC_RD_TIME, &rtc_tm);
	printf("%d-%d-%d %d:%d:%d\n", rtc_tm.tm_year, rtc_tm.tm_mon,
		rtc_tm.tm_mday, rtc_tm.tm_hour, rtc_tm.tm_min, rtc_tm.tm_sec);
	close(rtc_fd);
	return 0;
}
