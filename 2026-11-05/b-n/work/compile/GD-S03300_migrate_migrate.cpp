#include <algorithm>
#include <fstream>
#include <bitset>
#include <string>
#include <vector>
#include <array>

#define fori(i,l,r) for(int i=(l);i<=(r);i++)
#define fori0(i,l,r) for(int i=(l);i<(r);i++)
#define ford(i,l,r) for(int i=(l);i>=(r);i--)
#define rgall(a)    (a).begin(),(a).end()
#define rgany(a,l,r) (a).begin()+(l),(a).begin()+(r)
#define rgcnt(a,n)  rgany(a,0,n)
#define rgo1(a,n)   rgany(a,1,n+1)
#define fr first
#define sc second

using namespace std;

ifstream cin("migrate.in");
ofstream cout("migrate.out");

array<long long,2000002> va,dpa,dpb,dpc;
array<int,2000002> vr;

int main(int argc,char* argv[])
{
    ios::sync_with_stdio(false);
    int testcase,T;
    cin>>testcase>>T;
    while(T--)
    {
        int n;
        long long m;
        cin>>n>>m;
        fori(i,1,n)
            cin>>va[i];
        va[0]=-4e18,va[n+1]=4e18,vr[0]=0;
        fori(i,1,n)
            vr[i]=upper_bound(rgo1(va,n),va[i]+m)-va.begin()-1;
        fori(i,1,n)//include s=t
        {
            ++dpa[i];
            if(vr[i]<=i)
            	continue;
			if(vr[i-1]<vr[i])
                dpa[vr[i]]+=dpa[i]-1;
            ++dpa[vr[i]];
        }
        ford(i,n,1)
        {
            ++dpc[i];
            if(vr[i]>i&&vr[i-1]<vr[i])
                dpc[i]+=dpc[vr[i]]+(vr[i]-max(vr[i-1],i)-1);
        }
        fori(i,1,n-2)
        {
        	if(vr[i]<=i+1)
        		continue;
            if(vr[i-1]<vr[i]-1)
                dpb[vr[i]]+=dpa[i]-1;
            ++dpb[vr[i]];
		}
        long long ans=0;
        fori(i,2,n)
        {
            if(vr[i]<=i||vr[i-1]<i||vr[i-2]==vr[i])
                continue;
            if(vr[i-1]==vr[i])
            	ans+=(dpc[vr[i]]-1)*dpb[i];
            ans+=(vr[i-1]-max(vr[i-2],i))*dpb[i];
        }
        cout<<ans<<'\n';
//        fori(i,1,n)
//        	cout<<dpa[i]<<' ';
//        cout<<endl;
//        fori(i,1,n)
//        	cout<<dpb[i]<<' ';
//        cout<<endl;
//        fori(i,1,n)
//        	cout<<dpc[i]<<' ';
//        cout<<endl;
        fori(i,0,n+1)
            va[i]=dpa[i]=dpb[i]=dpc[i]=vr[i]=0;
    }//Remember CLEAR!
    return 0;//when dp check trans connectivity
}

//16:15 -> 17:16

/*
0 2
5 3
-2 -1 0 1 2
6 2
-4 -3 -2 -1 3 6
*/

//notice diconnected

/*
when coding check the following

two path: abd acd , c=b-1
s->a->(b-1,b)->c->t
s->a,c->t only i->r_i
s->a,c->t only 1
a->c only 2
s->a i->r_i
a->c=r_r_a check b-1,b-2
c->t i->r_i

val_c count t:c have unique path to t
val: val+=(r_{c-1}+1,r_c); c <- r_c  =>  val_c=(r_c-r_{c-1})+val_{r_c}

vbl_a count s with i->r_i to a

to check:
s->a i->r_i (vbl_a)
a->(b-1,b=r_a)->c=r_b
NO b-2->c
NO a-1->b-1
c->t i->min(r_i,t) (val_c)

enumerate (a,b,c) O(n) is sufficient.

r[b]==r[b-1]==c!=r[b-2]
r[a-1]<b-1

specially get a and c not regular,only 1 step

(s,s->a)->(b-1,b)->(t,c->t)

t:b b-1 reach, b-2 not
c->t:val

dp val on b,b count c or t

when t not regular no r[b]==r[b-1]
*/
