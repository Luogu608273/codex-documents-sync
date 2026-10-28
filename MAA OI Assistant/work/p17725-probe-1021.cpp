#define main user_main
#include "p17725-user-debug-1021.cpp"
#undef main
#include <vector>
void probe(vector<int> ar){
 n=ar.size();
 for(int i=1;i<=n;i++) a[i]=ar[i-1],mn[i]=0;
 for(int i=1;i<n;i++){
  hgb[i]=highbit(a[i]^a[i+1]);
  if(hgb[i]!=-1)hgv[i]=a[i]&hgb[i];
 }
 ans=1;v1=v2=0;
 for(int i=1;i<n;i++){
  f[i]=ans;
  if(hgb[i]==-1)continue;
  if((v1&hgb[i])&&(v2&hgb[i])!=hgv[i])ans++,v1=v2=0;
  else v1|=hgb[i],v2|=hgv[i];
 }
 f[n]=ans;
 for(int i=1;i<n;i++){
  v1=v2=0;int low=1<<30;
  for(int j=i-1;j>=0;j--){
   if(hgb[j]!=-1&&(v1&hgb[j])&&(v2&hgb[j])!=hgv[j])break;
   if(f[j]<f[i]-1)break;
   if(f[j]==f[i]-1){
    int nv2=v2^a[i],nl=a[i]^a[j+1],m1=mn[j]-1;
    clean_dfs();int z=dfs(29,0,m1,nl,v1,nv2);
    if(low<z){
     cout<<"overwrite a:";for(int k=1;k<=n;k++)cout<<' '<<a[k];
     cout<<" i="<<i<<" j="<<j<<" min="<<low<<" now="<<z<<'\n';exit(0);
    }
    if(z>=0)low=min(low,z);mn[i]=z;
   }
   if(hgb[j]!=-1)v1|=hgb[j],v2|=hgv[j];
  }
 }
}
int main(){
 for(int len=2;len<=8;len++){
  int cnt=1<<(len*2);
  for(int z=0;z<cnt;z++){
   vector<int> ar(len);int q=z;
   for(int &x:ar)x=q%4,q/=4;
   probe(ar);
  }
 }
}
