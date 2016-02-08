#include <pthread.h>
#include <stdio.h>
#include<sys/time.h>
#include <stdlib.h>
//#define NUM_THREADS 8 
//#define cpu_paranum_iteration 10000000000.0
int NUM_THREADS=8;
long cpu_paranum_iteration=10000000000;
struct arr
{
long f1,f2;
};

struct arr ar[10];
struct arr ar1[10];
struct timeval1 {
  long tv_sec;  /* seconds since 00:00:00 GMT 1/1/1970 */
  long tv_usec; /* microseconds */
};
struct timezone1 {
  int tz_minuteswest; /* west of GMT */
  int tz_dsttime;     /* set if daylight saving time in affect */
};

void *gflops(void *threadid)
{

struct timeval startTime,endTime;
struct timezone1 *tzp1,*tzp2;
long int i=0,sum_int1=0;
//long int cpu_paranum_iteration=1000000000;
double sum_dou1=0,double_var=2.4324,d=15.2,b=34.123,c=534.6453;
double a=90.1,e=75.2,f=5.23,g=9.1,h=5.7,k=82.1,l=23.3,m=142.1,n=12.3;
long tid;
tid=(long)threadid;

gettimeofday(&startTime,NULL);
//printf("%ld \n",startTime.tv_sec);
//long int i=0;
register r1=1.2,r2=2.3,r3=1.2; 
for(i=0;i< (cpu_paranum_iteration/(40*NUM_THREADS));i++)
        {
          //      sum_dou1= double_var+3.421+5.3213;
	//	r1=double_var+d;
	//	r2=b+c;
	//	r3=d+c;
	//	r4=double_var+b;                
	
 /*       a+c;h*f;d*e;k*l;
	b+c;
	c+c;
	a+a;
	b+b;
	a+b;	e+f;g+h;a+d;
*/	a-b;c-d;e-f;g-h;k-l;m-n;
        a/b;c/d;e/f;g/h;k/l;m/n;
        a+b;c+d;e+f;g+h;k+l;m+n;
        a*b;c*d;e*f;g*h;k*l;m*n;
        a-b;c-d;e-f;g-h;k-l;m-n;
	a+h;a+k;a+l;a+m;a+n;b+h;
	b/c;d/e;f/g;h/k;l/m;
	b*c;d*e;f*g;h*k;l*m;
/*
b+d;
b+k;
b+l;
b+m;
b+n;
c+d;
c+e;
c+f;
c+g;
c+h;
c+k;
c+l;
c+m;
c+n;
*/
	//r2+r3;
        }
gettimeofday(&endTime,NULL);

ar[tid].f1=(startTime.tv_sec)*1000000 + startTime.tv_usec;
ar[tid].f2=(endTime.tv_sec)*1000000 + endTime.tv_usec;
//printf("the no of flops is %f\n",f);

 pthread_exit(NULL);
}


void *gilops(void *threadid)
{

struct timeval startTime,endTime;
struct timezone1 *tzp1,*tzp2;
long int i=0;
long tid;
tid=(long)threadid;

int d=15,b=34,c=534;
int a=90,e=75,f=5,g=9,h=5,k=82,l=23,m=142,n=12;


gettimeofday(&startTime,NULL);
for(i=0;i< (cpu_paranum_iteration/(40*NUM_THREADS));i++)
{
	a-b;c-d;e-f;g-h;k-l;m-n;
        a/b;c/d;e/f;g/h;k/l;m/n;
        a+b;c+d;e+f;g+h;k+l;m+n;
        a*b;c*d;e*f;g*h;k*l;m*n;
        a-b;c-d;e-f;g-h;k-l;m-n;
	a+h;a+k;a+l;a+m;a+n;b+h;
	b/c;d/e;f/g;h/k;l/m;
	b*c;d*e;f*g;h*k;l*m;
}
gettimeofday(&endTime,NULL);

ar1[tid].f1=(startTime.tv_sec)*1000000 + startTime.tv_usec;
ar1[tid].f2=(endTime.tv_sec)*1000000 + endTime.tv_usec;
//printf("the no of flops is %f\n",f);

 pthread_exit(NULL);
}


int main (int argc, char *argv[])
{
//	if((argc!=0 )&& (argv[2]!=0))   
//	{	NUM_THREADS=argv[2];  }

printf("enter the number of threads");
scanf("%d",&NUM_THREADS);
	pthread_t threads[NUM_THREADS];
   	int rc;
	void *status;
   	long t;
struct timeval startTime,endTime,start,end;
gettimeofday(&startTime,NULL);

   for(t=0; t<NUM_THREADS; t++){
      printf("In main: creating thread for gflops %ld\n", t);
      rc = pthread_create(&threads[t], NULL, gflops, (void *)t);
      if (rc){
         printf("ERROR; return code from pthread_create() is %d\n", rc);
         exit(-1);
      }
}
for(t=0;t<NUM_THREADS;t++)
{
pthread_join(threads[t],&status);
	
}

gettimeofday(&endTime,NULL);

printf("in main\n");
//printf("the final loop \n");
printf("startime is %ld sec %ld msec\n",startTime.tv_sec,startTime.tv_usec);
printf("endtime id %ld sec %ld msec\n",endTime.tv_sec,endTime.tv_usec);
long diff  = (endTime.tv_sec-startTime.tv_sec)*1000000 + (endTime.tv_usec-startTime.tv_usec);
printf("the difference is %lf\n",(double)diff/1000000);
double f;
long q=(cpu_paranum_iteration);//NUM_THREADS);
double w=(diff/1000000.0);
//w=w/1000000000;
//f=(double)q/w;
//printf("the no of flops is %lf\n",f);

int i,j;
/*for(i=0;i<NUM_THREADS;i++)
{
printf("the first loop flops is %ld\n",ar[i].f1);
printf("the second loop flops is %ld\n",ar[i].f2);
}*/

long s,e;
s=ar[0].f1;
e=ar[0].f2;
for(j=1;j<NUM_THREADS;j++)
  {
  	if(ar[j].f1<s)
   		s=ar[j].f1;
   	if(ar[j].f2>e)
    		e=ar[j].f2;
}
printf("in loops\n");
//printf("the final loop \n");
printf("lowest startime is %ld msec\n",s);
printf("highest endtime is %ld msec\n",e);

double d=((double)(e-s))/1000000.0;

printf("%ld\n",e-s);
printf("time difference in sec %lf\n",d);
double g=(double)cpu_paranum_iteration;//*(double)NUM_THREADS;
double h=g/(d*1000000000.0);
printf("the total gflops is for %d threads is %lf\n",NUM_THREADS,h);
   
   
printf("\n  calculating the gilops now \n \n");
pthread_t ithreads[NUM_THREADS];
gettimeofday(&start,NULL);

   for(t=0; t<NUM_THREADS; t++){
      printf("In main: creating thread for gilops %ld\n", t);
      rc = pthread_create(&ithreads[t], NULL, gilops, (void *)t);
      if (rc){
         printf("ERROR; return code from pthread_create() is %d\n", rc);
         exit(-1);
      }
}
for(t=0;t<NUM_THREADS;t++)
{
pthread_join(ithreads[t],&status);
	
}

gettimeofday(&end,NULL);

printf("in main\n");
//printf("the final loop \n");
printf("startime is %ld sec %ld msec\n",start.tv_sec,start.tv_usec);
printf("endtime id %ld sec %ld msec\n",end.tv_sec,end.tv_usec);
long diff1  = (end.tv_sec-start.tv_sec)*1000000 + (end.tv_usec-start.tv_usec);
printf("the difference is %lf\n",(double)diff1/1000000);

long s1,e1;
s1=ar1[0].f1;
e1=ar1[0].f2;
for(j=1;j<NUM_THREADS;j++)
  {
  	if(ar1[j].f1<s1)
   		s1=ar1[j].f1;
   	if(ar1[j].f2>e1)
    		e1=ar1[j].f2;
}
printf("in loops\n");
//printf("the final loop \n");
printf("lowest startime is %ld msec\n",s1);
printf("highest endtime is %ld msec\n",e1);

double d1=((double)(e1-s1))/1000000.0;

printf("%ld\n",e1-s1);
printf("time difference in sec %lf\n",d1);
double g1=(double)cpu_paranum_iteration;//*(double)NUM_THREADS;
double h1=g1/(d1*1000000000.0);
printf("the total gilops is for %d threads is %lf\n",NUM_THREADS,h1);

/* Last thing that main() should do */

pthread_exit(NULL);
}
