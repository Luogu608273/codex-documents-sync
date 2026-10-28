#define main user_main
#include "p17725-user-debug-1021.cpp"
#undef main
int main(){
 int m=2,l=0,x=3,y=1;
 clean_dfs();cout<<dfs(1,0,m,l,x,y)<<'\n';
}
