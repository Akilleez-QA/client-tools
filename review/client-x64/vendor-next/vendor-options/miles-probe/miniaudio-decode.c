#include "../miniaudio.h"
#include <stdio.h>
int main(int argc,char **argv) {
 if(argc!=3)return 2;ma_decoder d;ma_decoder_config cfg=ma_decoder_config_init(ma_format_s16,0,0);
 ma_result r=ma_decoder_init_file(argv[1],&cfg,&d);if(r!=MA_SUCCESS){printf("init=%d\n",r);return 3;}
 FILE *f=fopen(argv[2],"wb");if(!f)return 4;ma_int16 buffer[8192];ma_uint64 total=0,read=0;
 do {r=ma_decoder_read_pcm_frames(&d,buffer,8192/d.outputChannels,&read);fwrite(buffer,sizeof(ma_int16)*d.outputChannels,(size_t)read,f);total+=read;}while(read>0);
 printf("channels=%u rate=%u frames=%llu final=%d\n",d.outputChannels,d.outputSampleRate,(unsigned long long)total,r);fclose(f);ma_decoder_uninit(&d);return r==MA_AT_END||r==MA_SUCCESS?0:5;
}
