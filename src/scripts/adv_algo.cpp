#include<cstdio>
#include<list>
#include<vector>
#include<queue>

using namespace std;

#define pld pair<long,double>

class Graph{

	public:
	       	vector<list<pld>> adj,rAdj;
		list<long> topOrder;

	Graph(int n){
		adj.resize(n);
		rAdj.resize(n);
	}
};


class Funnel{
	public:
	 	Graph fg;

	Funnel(int n){
		fg=Graph(n);
		}

};


void build_funnel(Graph &G, Funnel &f, long root){
	
}

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
			m++;
		}

		printf("N%ld M%ld\n",n,m);
		
		comp_topOrder(G);
		print_topOrder(G);
		
		// Funnel Graphs
		Funnel f = Funnel(n);
		list<long> :: iterator it;
		for(it=G.topOrder.begin();it!= G.topOrder.end();it++){
			build_funnel(G,f,*it);
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
