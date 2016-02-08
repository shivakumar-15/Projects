#include<stdio.h>
#include<stdlib.h>
#include<sys/time.h>
#include<string.h>
#include<cuda.h>

__global__ void funcflops(float *a,float *b,float *c)
{
int t=blockIdx.x*blockDim.x+threadIdx.x;
c[t]=a[t]+b[t]+1;
c[t+2]=a[t+2]*b[t+2];
c[t]=a[t]+b[t];
c[t]=a[t]+b[t];
c[t]=a[t]+b[t];
//c[t]=a[t]*b[t];
//c[t]=a[t]-b[t];
//c[t]=a[t]/b[t];
}

int main( void )
{

int cyclecount=10000;
int devicecount,device;
double time_s;
int blocks,threads,n;
long start_time,end_time;
struct cudaDeviceProp properties;
float *a, *b, *c;
struct timeval start,stop;
float *dev_a, *dev_b, *dev_c;
cudaError_t cudaResultCode = cudaGetDeviceCount(&devicecount);
if (cudaResultCode != cudaSuccess)
    devicecount = 0;
/* machines with no GPUs can still report one emulation device */
for (device = 0; device < devicecount; ++device) {
    cudaGetDeviceProperties(&properties, device);
    if (properties.major != 9999) /* 9999 means emulation only */
    if (device==0)
    {
            printf("multiProcessorCount %d\n",properties.multiProcessorCount);
            printf("maxThreadsPerMultiProcessor %d\n",properties.maxThreadsPerMultiProcessor);
            blocks=properties.multiProcessorCount;
            threads=properties.maxThreadsPerMultiProcessor;
//            n=properties.multiProcessorCount * properties.maxThreadsPerMultiProcessor;
	    n=blocks*threads;  
  }
}
printf("%s\n",properties.name);
a=(float*)malloc(n * sizeof(float));
b=(float*)malloc(n * sizeof(float));
c=(float*)malloc(n * sizeof(float));

 // allocate the memory on the GPU
cudaMalloc( (void**)&dev_a, n * sizeof(float) );
cudaMalloc( (void**)&dev_b, n * sizeof(float) );
cudaMalloc( (void**)&dev_c, n * sizeof(float) );
 // fill the arrays 'a' and 'b' on the CPU
 for (int i=0; i<n; i++) {
 a[i] = -i;
 b[i] = i * i;
 }
cudaMemcpy( dev_a, a, n * sizeof(int),cudaMemcpyHostToDevice );
cudaMemcpy( dev_b, b, n * sizeof(int),cudaMemcpyHostToDevice );
gettimeofday(&start,NULL);
int i;
start_time=start.tv_sec*1000000 + start.tv_usec;//get start time
for(i=0;i<cyclecount;i++)
 funcflops<<<blocks,threads>>>( dev_a, dev_b, dev_c );
gettimeofday(&stop,NULL);
end_time=stop.tv_sec*1000000 + stop.tv_usec;//get end time
 // copy the array 'c' back from the GPU to the CPU
cudaMemcpy( c, dev_c, n * sizeof(int),cudaMemcpyDeviceToHost );
 // display the results
// for (int i=0; i<N; i++) {
// printf( "%d + %d = %d\n", a[i], b[i], c[i] );
// }
 // free the memory allocated on the GPU
time_s=end_time-start_time;
printf("Time taken: %lf\n",time_s);
//printf("GFLOPS: %lf\n",);
double d=(double)(cyclecount*n*5)/((double)time_s*1000.0);
//d=d/1000000.0;
printf("GFlops  %lf \n",d);
 cudaFree( dev_a );
 cudaFree( dev_b );
 cudaFree( dev_c );
 return(0);
}

