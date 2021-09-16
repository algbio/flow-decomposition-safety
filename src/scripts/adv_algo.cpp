/* 
 * Todo: 
 * 1- Time Efficient exist edge using Maps?
 * 2- Space Efficient Funnels using Maps?
 * 3- Complete flow code for non max
 * 4- Complete flow code for reporting maximal
 *
 */


#include<cstdio>
#include<list>
#include<vector>
#include<queue>
#include<algorithm>

using namespace std;

#define pld pair<long,double>
#define pdl pair<double,long>

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

class Funnel{
	public:
	 	Graph fg;

	void addEdge(long a, long b, double c){
		fg.adj[a].push_back(pld(b,c));
		fg.rAdj[b].push_back(pld(a,c));
		fg.fIn[b] += c;
	}
	
	Funnel(int n){
		fg=Graph(n);
		}

};

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


void build_funnel(Graph &G, vector<Funnel> &f, long root){
	list<pld> :: iterator it;
	
	vector<pdl> outN;
	pld max = pld(-1,0);
	for(it=G.adj[root].begin();it!=G.adj[root].end();it++){
		f[(*it).first].addEdge(root,(*it).first,(*it).second);
	
		outN.push_back(pdl((*it).second,(*it).first));

		if(max.second <= (*it).second){
			if(max.second == (*it).second) max.first=-2;
			else 			       max=*it;
		}
	}

	//         Make funnel of Max out neighbour and safeF for all
	vector<long> safeF = vector<long>(G.adj.size(),0);
	vector<int> vis = vector<int>(G.adj.size(),0);
	revReachTopOrder(f[root].fg,root,vis);
	
	safeF[root] = max.second; // Use max weight even if duplicate
	list<long> :: iterator itx;
	for(itx=f[root].fg.topOrder.begin();itx!=f[root].fg.topOrder.end();itx++){
		for(it=f[root].fg.rAdj[*itx].begin();it!=f[root].fg.rAdj[*itx].end();it++){
			if(safeF[(*it).first]< safeF[*itx] - G.fIn[*itx] + (*it).second)
				safeF[(*it).first] = safeF[*itx] - G.fIn[*itx] + (*it).second;
			if((max.first!=-2) && (safeF[*itx] - G.fIn[*itx] + (*it).second > 0) &&
					!existEdge(f[max.first].fg,*itx,(*it).first)) 
				f[max.first].addEdge(*itx,(*it).first,(*it).second);
		}
	}

	// Make funnel of rest of the neighbours
	list<pld> Ns, Np;
	list<pld> :: iterator its;
	sort(outN.begin(),outN.end()); //,greater<pdl>());
	for(int i=0;i < outN.size();i++){
		if(outN[i].second== max.first) break;
		Ns.push_back(pld(outN[i].second,outN[i].first));
		Np.push_back(pld(outN[i].second,outN[i].first));
		Np.push_back(outN[i].second);
	}	

	long x,y=root;
	list<long> path;
	path.push_back(root);

	while(!Np.empty()){
	//for(itx=Np.begin(); itx!= Np.end();itx++){
		// Max weight edge to y
		pld maxY=pld(-1,0);
		for(it=f[root].fg.rAdj[y].begin();it!= f[root].fg.rAdj[y].end();it++){
			if(maxY.second<= (*it).second) {
				maxY = *it;	// Choose any if duplicate
			}
		}

		x= maxY.first;	
		path.push_front(x);

		for(its=Ns.begin();its!=Ns.end();its++){
		     if(safeF[x]-max.second+(*its).second> 0 && 
				!existEdge(f[(*its).first].fg,x,y))
				f[(*its).first].addEdge(x,y,maxY.second);
		     else its = Ns.erase(its);
		}
		
	
	}
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

int main(int argc, char *argv[]){
	char line[100];
	long n,m,graphC=0;
	//int t=10;

	

	int flag=0;
	if(argc==2){
		if(argv[1][0]=='a') flag=1;// all paths + stats
		if(argv[1][0]=='s') flag=2;// stats only	
	}

	while(scanf("%[^\n]",line) > 0){
		if(flag<2) printf("%s\n",line);
		graphC++;
		scanf("%ld",&n);
		m=0;

		Graph G= Graph(n);
		long a,b;
		double c;

		while(scanf("%ld %ld %lf\n",&a,&b,&c)> 0){	
			G.adj[a].push_back(pld(b,c));
			G.rAdj[b].push_back(pld(a,c));	
			G.fIn[b]+= c;
			m++;
		}

		printf("N%ld M%ld\n",n,m);
		
		comp_topOrder(G);
		print_topOrder(G);
		
		// Funnel Graphs
		vector<Funnel> f;
		f.resize(n,Funnel(n));
		list<long> :: iterator it;
		for(it=G.topOrder.begin();it!= G.topOrder.end();it++){
		//	build_funnel(G,f,*it);
		}
	
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
