#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/time.h>
#define num_mem_block 1000
#define mem_block_size 1048576
#define NUM_THREADS 1

int z=0,y=0;

struct mem
{
long t;
};

struct arr
{
long f1,f2;
};

struct arr ar1[10],ar2[10];


void func(char** m) //int mem_block_size
{
//char** m = mg;
struct timeval start,end;
int i;
	char* temp;
	gettimeofday(&start, 0x0);
	for(i = 0;i < num_mem_block;i++)
	{
		temp = strchr(m[i], '1');
	}
for(i = 0;i < num_mem_block;i++)
	{
		memset(m[i], '0', mem_block_size);
	}

gettimeofday(&end,NULL);
/*printf("in func \n start time %ld msec\n",start.tv_sec*1000000+start.tv_usec);
printf("end time %ld msec\n",end.tv_sec*1000000+end.tv_usec);
*/
long diff  = (end.tv_sec-start.tv_sec)*1000000 + (end.tv_usec-start.tv_usec);
printf("diff in msec %ld\n",diff);

double f1=(double)mem_block_size*(double)num_mem_block;
double f2=(double)diff/1000000.00;
double f3=f1/f2;
//f3=f3/1000000.00;
ar1[z].f1=(start.tv_sec)*1000000 + start.tv_usec;
ar1[z].f2=(end.tv_sec)*1000000 + end.tv_usec;
z++;
pthread_exit(NULL);

}

void randfunc(char** m) //int mem_block_size
{
//char** m = mg;
struct timeval start,end;
long i, *ran;
	char* temp;
	
	time_t t;
	srand((unsigned)time(&t));
	ran = (long*)malloc(sizeof(long) * num_mem_block);
	for(i = 0;i < num_mem_block;i++)
	{
		ran[i] = rand() % num_mem_block;
	}	
	gettimeofday(&start, 0x0);
	for(i = 0;i < num_mem_block;i++)
	{
		temp = strchr(m[ran[i]], '1');
	}
for(i = 0;i < num_mem_block;i++)
	{
		memset(m[ran[i]], '0', mem_block_size);
	}

gettimeofday(&end,NULL);
/*printf("in func \n start time %ld msec\n",start.tv_sec*1000000+start.tv_usec);
printf("end time %ld msec\n",end.tv_sec*1000000+end.tv_usec);
*/
long diff  = (end.tv_sec-start.tv_sec)*1000000 + (end.tv_usec-start.tv_usec);
printf("diff in msec %ld\n",diff);

double f1=(double)mem_block_size*(double)num_mem_block;
double f2=(double)diff/1000000.00;
double f3=f1/f2;
//f3=f3/1000000.00;
ar2[y].f1=(start.tv_sec)*1000000 + start.tv_usec;
ar2[y].f2=(end.tv_sec)*1000000 + end.tv_usec;
y++;
pthread_exit(NULL);

}

void* mem_test(void* arg)
{
	struct mem mem_para = *((struct mem*)arg);
	long id = mem_para.t;
	//long num_mem_block = mem_para.num_mem_block;
	//long mem_block_size = mem_para.mem_block_size;
	char** mem_char;
	mem_char = (char**)malloc(sizeof(char*) * num_mem_block);
	long i;
	for(i = 0;i < num_mem_block;i++)
	{
		mem_char[i] = (char*)malloc(mem_block_size);
	}
	for(i = 0;i < num_mem_block;i++)
	{
		memset(mem_char[i], '0', mem_block_size - 1);
		mem_char[i][mem_block_size - 1] = '1';
	}
	func(mem_char);
	
for(i = 0;i < num_mem_block;i++)
	{
		free(mem_char[i]);
	}
	free(mem_char);
	return NULL;
}

void* mem_test1(void* arg)
{
	struct mem mem_para = *((struct mem*)arg);
	long id = mem_para.t;
	//long num_mem_block = mem_para.num_mem_block;
	//long mem_block_size = mem_para.mem_block_size;
	char** mem_char;
	mem_char = (char**)malloc(sizeof(char*) * num_mem_block);
	long i;
	for(i = 0;i < num_mem_block;i++)
	{
		mem_char[i] = (char*)malloc(mem_block_size);
	}
	for(i = 0;i < num_mem_block;i++)
	{
		memset(mem_char[i], '0', mem_block_size - 1);
		mem_char[i][mem_block_size - 1] = '1';
	}
	randfunc(mem_char);
	
for(i = 0;i < num_mem_block;i++)
	{
		free(mem_char[i]);
	}
	free(mem_char);
	return NULL;
}

void main()
{
int j=0;
int i=0;
struct timeval start,end,start1,end1;

int c;

pthread_t threads[NUM_THREADS];
int rc;
void *status;
long t;

gettimeofday(&start,NULL);

   for(t=0; t<NUM_THREADS; t++)
{
	struct mem *m1=(struct mem *)malloc(sizeof(struct mem *));
	m1->t=t;	
	//strncpy(m1->mem_char,mem,mem_block_size);
	printf("In main: creating thread %ld\n", t);
	rc = pthread_create(&threads[t], NULL,mem_test, (void *)m1);
	if (rc)
	{
	         printf("ERROR; return code from pthread_create() is %d\n", rc);
	         exit(-1);
	}
}
for(t=0;t<NUM_THREADS;t++)
{
pthread_join(threads[t],&status);

}
 
gettimeofday(&end, NULL);
/*
printf("in main\n start time %ld\n",start.tv_sec*1000000+start.tv_usec);	
printf("end time %ld\n",end.tv_sec*1000000+end.tv_usec);
long diff  = (end.tv_sec-start.tv_sec)*1000000 + (end.tv_usec-start.tv_usec);
double d=(double)diff/1000000.0;
printf("diff in micro sec %lf\n",d);
double f1=(((double)mem_block_size*(double)num_mem_block)/NUM_THREADS)/(double)d;
printf(" \n the thoughput %lf\n",f1);
*/
/*
for(i=0;i<NUM_THREADS;i++)
{
printf("the first loop flops is %ld\n",ar1[i].f1);
printf("the second loop flops is %ld\n",ar1[i].f2);
}*/
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
printf("lowest startime is %ld msec\n",s1);
printf("highest endtime is %ld msec\n",e1);
double d1=((double)(e1-s1))/1000000.0;

printf("%ld\n",e1-s1);
printf("time difference in sec %lf\n",d1);
double f2=(((double)mem_block_size*(double)num_mem_block/(double)NUM_THREADS))/(double)d1;
f2=f2/1000000.0;
printf(" the thoughput %lf\n",f2);


printf(" \n\n\n random calculation\n\n\n");

gettimeofday(&start1,NULL);

   for(t=0; t<NUM_THREADS; t++)
{
	struct mem *m1=(struct mem *)malloc(sizeof(struct mem *));
	m1->t=t;	
	//strncpy(m1->mem_char,mem,mem_block_size);
	printf("In main: creating thread %ld\n", t);
	rc = pthread_create(&threads[t], NULL,mem_test1, (void *)m1);
	if (rc)
	{
	         printf("ERROR; return code from pthread_create() is %d\n", rc);
	         exit(-1);
	}
}
for(t=0;t<NUM_THREADS;t++)
{
pthread_join(threads[t],&status);

}
 
gettimeofday(&end1, NULL);
//printf("in main\n start time %ld\n",start1.tv_sec*1000000+start1.tv_usec);	
//printf("end time %ld\n",end1.tv_sec*1000000+end1.tv_usec);
/*long diff3  = (end1.tv_sec-start1.tv_sec)*1000000 + (end1.tv_usec-start1.tv_usec);
double d3=(double)diff3/1000000.0;
printf("diff in micro sec %lf\n",d3);
double f3=(((double)mem_block_size*(double)num_mem_block)/NUM_THREADS)/(double)d3;
printf(" \n the thoughput %lf\n",f3);
*/
/*
for(i=0;i<NUM_THREADS;i++)
{
printf("the first loop flops is %ld\n",ar1[i].f1);
printf("the second loop flops is %ld\n",ar1[i].f2);
}*/
long s,e;
s=ar2[0].f1;
e=ar2[0].f2;
for(j=1;j<NUM_THREADS;j++)
  {
  	if(ar2[j].f1<s)
   		s=ar2[j].f1;
   	if(ar2[j].f2>e)
    		e=ar2[j].f2;
}
printf("in loops\n");
printf("lowest startime is %ld msec\n",s);
printf("highest endtime is %ld msec\n",e);
double d4=((double)(e-s))/1000000.0;

printf("%ld\n",e-s);
printf("time difference in sec %lf\n",d4);
double f4=(((double)mem_block_size*(double)num_mem_block/(double)NUM_THREADS))/(double)d4;
f4=f4/1000000.0;
printf(" the thoughput %lf\n",f4);



pthread_exit(NULL);

}
