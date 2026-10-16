#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;
const int N = 2e5 + 10;
int t,n,k,p[N],fa[N],sz[N],s,lsz;
vector<int> ls;
bool b[30][30],b1[30],ans;
int fr(int u){if(u==fa[u])return u;return fa[u]=fr(fa[u]);}
void mg(int u,int v){u=fr(u),v=fr(v);fa[u]=v;}
int main(){
    cin>>t;
    while(t--){
        cin>>n>>k;ans=s=0;ls.clear();
        for(int i=1;i<=n;i++)fa[i]=i;
        for(int i=1;i<=n;i++){cin>>p[i];mg(p[i],i);sz[i]=0;}
        for(int i=1;i<=n;i++)sz[fr(i)]++;
        for(int i=1;i<=k;i++)b1[i]=0;
        b1[0]=1;
        for(int i=1;i<=n;i++)for(int j=k;j>=sz[i];j--)b1[j]|=b1[j-sz[i]];
        bool fg=0;
        for(int i=1;i<=k;i++)fg|=b1[i];
        if(fg==0){cout<<"Bob\n";continue;}
        for(int i=1;i<=n;i++)if(sz[i]>1)ls.push_back(sz[i]-1);
        sort(ls.begin(),ls.end(),greater<int>());
        b[0][0]=1;lsz=ls.size();
        for(int i=0;i<min(k,lsz);i++)s+=ls[i];
        if(s<=k)ans=1;
        for(int i=1;i<=min(k,lsz);i++){
            if(k+i-1<lsz)s+=ls[k+i-1];
            for(int j=0;j<min(k+i,lsz);j++)for(int l=k;l>=ls[j];l--)b[i][l]|=b[i-1][l-ls[j]];
            for(int l=k-i;l>=0;l--){ans|=(b[i][l]&&(s-l)<=k);if(ans)break;}
            if(ans)break;
        }
        if(ans){
            fg=0;int cnt=0;
            for(int i=1;i<=n;i++){if(sz[i]==k+1)fg=1;else cnt+=sz[i];}
            if(fg&&cnt>k&&cnt%(1+k)==0)cout<<"Bob\n";
            else cout<<"Alice\n";
        }else cout<<"Bob\n";
        for(int i=0;i<=min(k,lsz);i++)for(int j=0;j<=k;j++)b[i][j]=0;
    }
}
