#include <pcre.h>
#include <stdio.h>
#include <string.h>
int main(void) {
 int cases[]={0,1,10,11,20}; unsigned k; int checks=0;
 for(k=0;k<sizeof(cases)/sizeof(cases[0]);++k) {
  char pattern[128]="^",subject[32]=""; int i,errorOffset,result;
  const char *error=0; pcre *re;
  struct {int before; int slots[33]; int after;} output;
  for(i=0;i<cases[k];++i) {strcat(pattern,"(a)");strcat(subject,"a");}
  strcat(pattern,"$"); output.before=1234567; output.after=7654321;
  re=pcre_compile(pattern,0,&error,&errorOffset,0); if(!re)return 1;
  result=pcre_exec(re,0,subject,(int)strlen(subject),0,0,output.slots,33);
  if(result!=(cases[k]<=10?cases[k]+1:0))return 2; ++checks;
  if(output.before!=1234567||output.after!=7654321)return 3; ++checks;
  if(output.slots[0]!=0||output.slots[1]!=cases[k])return 4; ++checks;
  result=pcre_exec(re,0,"b",1,0,0,output.slots,33);
  if(result!=PCRE_ERROR_NOMATCH)return 5; ++checks;
  pcre_free(re);
 }
 printf("PASS %d bounded correct-count checks\n",checks);return 0;
}
