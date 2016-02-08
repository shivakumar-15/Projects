#include<stdio.h>
#include<stdlib.h>
#include<sys/time.h>
#include<string.h>
#include<cuda.h>

__global__ void funcflops(float *a,float *b,float *c)
{
int t=blockIdx.x*blockDim.x+threadIdx.x;
c[t]=a[t]+b[t];
}

int main( void )
{
int cyclecount=100000;
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
            n=properties.multiProcessorCount * properties.maxThreadsPerMultiProcessor;
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
int l;
start_time=start.tv_sec*1000000 + start.tv_usec;//get start time
for(l=0;l<cyclecount;l++)
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
printf("Time taken: %lf",time_s);
printf("GFLOPS: %lf",(double)(cyclecount*n*3)/(time_s*1000000000));

 cudaFree( dev_a );
 cudaFree( dev_b );
 cudaFree( dev_c );
 return(0);
}

