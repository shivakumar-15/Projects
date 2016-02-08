#include<stdio.h>
#include<stdlib.h>
#include<sys/time.h>
#include<string.h>
#include<cuda.h>

__global__ void func(int *a,int *b,int *c)
{
int t=blockIdx.x*blockDim.x+threadIdx.x;
c[t]=a[t]+b[t];
}

int main( void )
{

int mem_size=10000000;
long blocksize=1;
double t;
long s,e;
char *c;
int i=0;
struct timeval start,end;
char *dev_a;
c=(char *)malloc(blocksize*sizeof(char));
memset(c,'#',blocksize);
cudaMalloc( (void**)&dev_a, blocksize * sizeof(int) );
//cudaMalloc( (void**)&dev_b, n * sizeof(int) );

gettimeofday(&start,NULL);
s=start.tv_sec*1000000 + start.tv_usec;//get start time
for(i=0;i<(mem_size/blocksize);i++)
{
cudaMemcpy( dev_a, c, blocksize * sizeof(char),cudaMemcpyHostToDevice );
}
//cudaMemcpy( dev_b, b, n * sizeof(int),cudaMemcpyHostToDevice );

gettimeofday(&end,NULL);
e=end.tv_sec*1000000 + end.tv_usec;//get end time
 // copy the array 'c' back from the GPU to the CPU
t=e-s;
printf("Time taken: %lf",t);
double d=(double)mem_size/1000.0;
d=d/(double)t;
printf("throughput: %lf gb/s",d);

 cudaFree( dev_a );
 
 return(0);
}

