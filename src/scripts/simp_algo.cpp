/* 
 * Todo: 
 * 1- Time Efficient exist edge using Maps?
 * 2- Space Efficient Funnels using Maps?
 * 3- Complete flow code for non max
 * 4- Complete flow code for reporting maximal
 * 5- Remove non-right maximal paths from funnels
 */


#include<cstdio>
#include<climits>
#include<list>
#include<vector>
#include<queue>
#include<algorithm>
#include<cfloat>

using namespace std;

#define pld pair<long,double>
#define pdl pair<double,long>
#define pll pair<long,long>
#define pdd pair<double,double>
#define p3ld pair<pll,pld>
#define pddll pair<pdd,pll>
#define ipld list<pld>::iterator

class Graph{

	public:
	       	vector<list<pld>> adj,rAdj;
		list<long> topOrder;
		vector<double> fIn;

	Graph(int n=1){
		adj.resize(n);
		rAdj.resize(n);
		fIn.resize(n,0);
	}
};

int existEdge(Graph &G,long x, long y){
	list<pld> :: iterator it;
	for(it= G.adj[x].begin(); it!= G.adj[x].end(); it++)
		if((*it).first ==y) break;
	
	if(it== G.adj[x].end()) return 0;
	else			return 1;
}


void revReachTopOrder(Graph &G,long root,vector<int> &vis){
	list<pld> :: iterator it;

	for(it=G.rAdj[root].begin();it!=G.rAdj[root].end();it++){
		if(!vis[(*it).first]){
			vis[(*it).first]=1;
			revReachTopOrder(G,(*it).first,vis);
		}
	}	
	G.topOrder.push_back(root);
}

/*
void comp_topOrder(Graph &G){
	vector<long> indeg;
	queue<long> q;

	G.topOrder.clear();
	indeg.resize(G.adj.size());

	for(int i=0;i<G.adj.size();i++){
		indeg[i]=G.rAdj[i].size();
		if(!indeg[i]){
		       	G.topOrder.push_back(i);
			q.push(i);
		}
	}

	//printf("Q %lu\n",q.size());
	while(!q.empty()){
		long t = q.front(); 
		q.pop();
		list<pld> :: iterator it;
		for(it=G.adj[t].begin();it!=G.adj[t].end();it++){
			indeg[(*it).first]--;
			if(!indeg[(*it).first]){
				G.topOrder.push_back((*it).first);
				q.push((*it).first);
			}
		}
	}
	//printf("Top Ord %lu \n",G.topOrder.size());
}*/

void comp_topOrder(Graph &G){
	vector<int> vis;
	G.topOrder.clear();
	vis.resize(G.adj.size(),0);
	

	for(int i=0;i<G.adj.size();i++){
		if(G.adj[i].size()==0)
			revReachTopOrder(G,i,vis);
	}
}


void print_topOrder(Graph &G){
	list<long> :: iterator it;
	for(it=G.topOrder.begin();it!=G.topOrder.end();it++)
		printf("%ld ",*it);
	printf("\n");
}

void compute_unitigs(Graph &G, list<pair<list<ipld>,pld> > &paths, list<pair<list<ipld>,pld> > &unitigs){
	vector<long> secV = vector<long>(G.adj.size(),0);
	list<long>:: iterator it;
	list<pld> :: iterator edgit;	
	int prnt = 0;

	for(it=G.topOrder.begin(); it!=G.topOrder.end();it++){
		long x = *it;
		for(edgit=G.adj[x].begin(); edgit!= G.adj[x].end(); edgit++){
			long y= (*edgit).first;
			if(G.adj[y].size()==1 && G.rAdj[y].size()==1 && secV[y]==0){ // Begining of a unitig
			secV[y]=1;
			
			pld pth = pld(x,(*edgit).second);
			list<ipld> path;
			
			ipld curr = *it;
			while(true){
				if(pth.second > (*curr).second) 
					pth.second = (*curr).second;
				path.push_back(curr);

						if(G.adj[(*curr).first].size()==0) break;
						
						edgit2=G.adj[(*curr).first].begin(); 
						while((*edgit2).second== 0) edgit2++;
						curr = edgit2;
					}
					paths.push_back(pair<list<ipld>,pld>(path,pth));
					
			
		}
	}


		

}

	
void print_path_decomp(Graph &G, list<pair<list<ipld>,pld> > &paths){
	printf("Path decomposition %lu paths:\n", paths.size());
	
	list<pair<list<ipld>,pld> > :: iterator it;
	list<ipld> :: iterator it2;

	for(it=paths.begin();it!=paths.end();it++){
		printf("%lf %ld", (*it).second.second, (*it).second.first);
		for(it2=(*it).first.begin();it2!=(*it).first.end();it2++)
			printf(" %ld", (**it2).first);
		printf("\n");
	}
}





void updateG(Graph &G, list<ipld> &path, double val){
	list<ipld> :: iterator it;
	for(it=path.begin();it!=path.end();it++)
		(**it).second+= val;
}

void path_decomp(Graph &G, list<pair<list<ipld>,pld> > &paths){
	list<long> sources;
	list<pld> :: iterator edgit,edgit2;	
	double min=DBL_MAX;
	int prnt = 0;
	for(long i=0;i<G.adj.size();i++){
		if(G.rAdj[i].size()==0){ // Source node
			for(edgit=G.adj[i].begin(); edgit!= G.adj[i].end(); edgit++){
				while((*edgit).second!=0){// Source edge
					pld pth = pld(i,DBL_MAX);
					list<ipld> path;
					
					ipld curr = edgit;
					while(true){
						if(pth.second > (*curr).second) 
							pth.second = (*curr).second;
						path.push_back(curr);

						if(G.adj[(*curr).first].size()==0) break;
						
						edgit2=G.adj[(*curr).first].begin(); 
						while((*edgit2).second== 0) edgit2++;
						curr = edgit2;
					}
					paths.push_back(pair<list<ipld>,pld>(path,pth));
					if(prnt) printf("Path from %ld of %lf weight and length %lu added\n", 
							pth.first,pth.second, path.size());
					updateG(G,path,-1*pth.second);					
				}
			}
		}
	}

	list<pair<list<ipld>,pld> > :: iterator it;
	for(it=paths.begin();it!=paths.end();it++)
		updateG(G,(*it).first,(*it).second.second);
}


int main(int argc, char *argv[]){
	char line[100];
	long n,m,graphC=0;
	int prnt =0;
	//int t=10;

	int flag=0;
	if(argc==2){
		if(argv[1][0]=='a') flag=1;// all paths + stats
		if(argv[1][0]=='s') flag=2;// stats only	
		if(argv[1][0]=='e') flag=2;// extended unitigs	
	}

	while(scanf("%[^\n]",line) > 0){
		if(flag<2) printf("%s\n",line);
		graphC++;
		scanf("%ld",&n);
		m=0;

		Graph G= Graph(n);
		list<pair<list<ipld>,pld > > paths;
		list<pair<list<ipld>,pld > > unitigs;
		long a,b;
		double c;

		while(scanf("%ld %ld %lf\n",&a,&b,&c)> 0){	
			G.adj[a].push_back(pld(b,c));
			G.rAdj[b].push_back(pld(a,c));	
			G.fIn[b]+= c;
			m++;
		}

		if(prnt) printf("N%ld M%ld\n",n,m);
		
		path_decomp(G,paths);
		if(prnt) print_path_decomp(G,paths);

		compute_unitigs(G,paths,unitigs);
			  
		//comp_topOrder(G);
		//if(prnt) print_topOrder(G);
		
	
	//	printf("Orginal paths %ld, Final paths %ld, diff %ld\n", org,fin, org-fin );
	//	printf("Weight of Orginal paths %ld, Weight of Final paths %ld, diff %ld\n\n", wOrg,wFin, wOrg-wFin );
	}

	//if(flag){
	//	printf("\n\nNumber of Graphs processed: %ld\n", graphC);
	//	printf("Total Original Paths %ld, Total final Paths %ld, max diff %ld\n", tOrg, tFin, maxd);
	//	printf("Total Weight of Original Paths %ld, Total weight of final paths %ld, max diff %ld\n", wtOrg, wtFin, wMaxd);
	//}

	return 0;

	}
