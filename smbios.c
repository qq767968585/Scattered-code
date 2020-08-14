#include<stdio.h>
#include<unistd.h>
#include<sys/mman.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>

unsigned char* Search_Strs(unsigned char *p){
    char *str1="_SM_";
    char *str2="_DMI_";
    unsigned char *ptr;
    int j;
    ptr=p;
    for(;ptr<=p+0xffff;){  
        for(j=0;j<strlen(str1);j++){
            if(*(ptr+j)!=*(str1+j))
            break;
        }
        if(j>=strlen(str1)){   /*则已找到第一个字符串'_SM_',在其后16byte的5个byte是否是关键字'_DMI_'*/
          ptr+=0x10;   //地址加16个byte
          for(j=0;j<strlen(str2);j++){
            if(*(ptr+j)!=*(str2+j))
            break;
        }
        if(j>=strlen(str2)){   //找到第二个字符串'_DMI_'
            return p+0x18;       //SMBIOS结构表地址
        }
      }
     else{
      ptr+=0x10;   //没有找到第一个字符串，ptr+0x10重新search。
     }
    }
}



int main(){
    unsigned char* map_base
    int i;
    int fd;
    int *eps;
    unsigned char* bios_p;
    unsigned char* mem;
    unsigned char* bios_v;
    if((fd = open ("/dev/mem", O_RDONLY)) < 0)
    {
        perror ("open error");
        return -1;
    }

    mem = mmap (NULL, 256, PROT_READ, MAP_SHARED, fd, 0x000f0000);   // 把物理内存映射到虚拟内存上

    if (mem == MAP_FAILED)
    {
        perror ("mmap error:");
        return 1;
    }
    eps=(int*)(Search_Strs(mem));
    bios_p=(unsigned char*)(*eps);
    bios_v=bios_p+(*(bios_p+0x01));
    printf();

    return 0;
}