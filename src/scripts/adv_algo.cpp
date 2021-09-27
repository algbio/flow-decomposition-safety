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
#define pll pair<long,long>
#define pdd pair<double,double>
#define p3ld pair<pll,pld>
#define pddll pair<pdd,pll>


class LLHNode{
	public:
	double val;
	double upd;
	pll edg;

	LLHNode *left;
	LLHNode *right;
	int rank; // dist

	LLHNode(double v, double u, pll e){
	    this->val = v;
	    this->upd = u;
	    this->edg=e;

	    this->left=NULL;
	    this->right=NULL;
	    this->rank=0;
	}

};


class LazyLeftistHeap{
	void propUpd(LLHNode *root){
		if(root!=NULL && root->upd>0){
			if(root->left!=NULL)
				root->left->upd += root->upd;
			if(root->right!=NULL)
				root->right->upd+= root->upd;
			root->val+=root->upd;
			root->upd=0;
		}	
	}

	public: 
		LLHNode *root;
	
	LazyLeftistHeap(){
		root=NULL;
	}

	void merge(LazyLeftistHeap &heap){
		if (this == &heap)
			return;
		root = merge(root, heap.root);
		heap.root = NULL;
	}
	
	LLHNode* merge(LLHNode* h1, LLHNode * h2){
		if (h1 == NULL)	return h2;
		if (h2 == NULL)	return h1;
	 	
		propUpd(h1); // Lazy Update
		propUpd(h2); // Lazy Update

		if (h1->val > h2->val){
			LLHNode* t=h1; 
			h1=h2;h2=t;  // h1-> val < h2->val
		}
		
		if(h1-> left == NULL){
			h1->left = h2;
		}else {
			h1->right = merge(h1->right, h2);
			if(h1->left->rank < 
			   h1->right->rank){
				LLHNode* t= h1->left;
				h1->left= h1->right;
				h1->right=t;
			}
			h1->rank = h1->right->rank + 1;
		}
		return h1;
	}

	void insert(double v, double u, pll ed){
		root = merge(new LLHNode(v,u,ed),root);
	//	printf("Inserted %lf %lf %ld %ld\n",root->val,root->upd,root->edg.first,root->edg.second);
	}

	pddll findMin(){
//		if(root==NULL) 
//			return(pddll(pdd(-1,-1),pll(-1,-1)));
		return pddll(pdd(root->val,root->upd),root->edg);
	}

	void deleteMin(){
		propUpd(root);
		LLHNode* t=root;
		root = merge(root->left,root->right);
		delete t;
	}

	bool isEmpty(){
		return root==NULL;
	}

};

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
		list<p3ld> res;	

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


void opt_funnel(Graph &G, vector<Funnel> &f, long root){
	vector<LazyLeftistHeap> H= vector<LazyLeftistHeap>(G.adj.size());
	list<pld> :: iterator it;
 	printf("Build Funnel %ld\n",root);	

	for(it=f[root].fg.adj[root].begin();it!=f[root].fg.rAdj[root].end();it++){
		H[(*it).first].insert((*it).second,-1,pll((*it).first,root));
	}

	double updM=0,maxUp=-1;   // maxUpdate val
	for(it=G.adj[root].begin();it!=G.adj[root].end();it++){
		updM+= (*it).second;
		if(maxUp< (*it).second) maxUp=(*it).second;
	}
	updM-= maxUp; // TODO:: CONDITION FOR SINK?

	vector<int> vis = vector<int>(G.adj.size(),0);
	revReachTopOrder(f[root].fg,root,vis);

	list<long> :: iterator itx;
	itx=f[root].fg.topOrder.end(); itx--; itx--;
	while(itx!=f[root].fg.topOrder.begin()){
		for(it=f[root].fg.rAdj[*itx].begin();it!=f[root].fg.rAdj[*itx].end();it++){
			double upd = f[root].fg.fIn[*itx]- (*it).second;

			if(!H[*itx].isEmpty()){
				if(H[*itx].root->upd==-1){
					if(f[root].fg.adj[(*it).first].size()==1){ // TODO:: Resolve for extFunnel
						H[(*it).first].insert(H[*itx].root->upd - upd,-1,pll((*it).first,*itx));
					}else{
						H[(*it).first].insert(H[*itx].root->upd,-1,pll((*it).first,*itx));
					
					}
				}else{
				

				}			
			}

	      itx--;
	}	


}


void build_funnel(Graph &G, vector<Funnel> &f, long root){
	list<pld> :: iterator it;
 	printf("Build Funnel %ld\n",root);	
	vector<pdl> outN;
	pld max = pld(-1,0);
	for(it=G.adj[root].begin();it!=G.adj[root].end();it++){
		f[(*it).first].addEdge(root,(*it).first,(*it).second);

		printf("outN Add F%ld (%ld,%ld)\n", 
				(*it).first,root,(*it).first);	
		outN.push_back(pdl((*it).second,(*it).first));

		if(max.second <= (*it).second){
			if(max.second == (*it).second) max.first=-2;
			else 			       max=*it;
		}
	}

	//         Make funnel of Max out neighbour and safeF for all
	vector<double> safeF = vector<double>(G.adj.size(),0);
	vector<int> vis = vector<int>(G.adj.size(),0);
	revReachTopOrder(f[root].fg,root,vis);

	safeF[root] = max.second; // Use max weight even if duplicate
	list<long> :: iterator itx;
	itx=f[root].fg.topOrder.end(); itx--;
	while(itx!=f[root].fg.topOrder.begin()){

	//for(itx=f[root].fg.topOrder.egin();itx!=f[root].fg.topOrder.end();itx++){
		for(it=f[root].fg.rAdj[*itx].begin();it!=f[root].fg.rAdj[*itx].end();it++){
			if(safeF[(*it).first]< safeF[*itx] - G.fIn[*itx] + (*it).second)
				safeF[(*it).first] = safeF[*itx] - G.fIn[*itx] + (*it).second;
			//printf("Try maxV Add F%ld (%ld,%ld) %lf-%lf+%lf %d\n", 
			//		max.first,(*it).first,*itx,safeF[*itx], G.fIn[*itx], (*it).second ,
			//		existEdge(f[max.first].fg,(*it).first,*itx));	

			if((max.first!=-2) && (safeF[*itx] - G.fIn[*itx] + (*it).second > 0) &&
					!existEdge(f[max.first].fg,(*it).first,*itx)){ 
				f[max.first].addEdge((*it).first,*itx,(*it).second);
	
				printf("maxV Add F%ld (%ld,%ld)\n", 
					max.first,(*it).first,*itx);	
			
			}
		}
	      itx--;
	}	

	// Make funnel of rest of the neighbours
	list<pld> Ns, Np;
	list<pld> :: iterator its;
	sort(outN.begin(),outN.end()); //,greater<pdl>());
	for(int i=0;i < outN.size();i++){
		if(outN[i].second== max.first) break;
		Ns.push_back(pld(outN[i].second,outN[i].first));
		Np.push_back(pld(outN[i].second,outN[i].first));
	}	

	long x,y=root;
	list<pld> path;
	path.push_back(pld(root,0));

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
		path.push_front(maxY);

		for(its=Ns.begin();its!=Ns.end();its++){
		     if(x!=-1 && safeF[x]-max.second+(*its).second> 0 && 
				!existEdge(f[(*its).first].fg,x,y)){
				f[(*its).first].addEdge(x,y,maxY.second);
		    		printf("suff Add F%ld (%ld,%ld)\n", 
					(*its).first,x,y);			     
		     }
		     else its = Ns.erase(its);
		}
		
		while(!Np.empty() && (x==-1 || 
		  safeF[x]-max.second+Np.front().second<0)){
			pld top = Np.front();
			Np.pop_front();
			list<pld> :: iterator iyp;  // y' in paper
			iyp= path.begin();
			iyp++;
			
			while(f[top.first].fg.adj[(*iyp).first].empty()){
				long a=(*iyp).first,b;
				double c=(*iyp).second;
				iyp++;
				b=(*(iyp)).first;
				f[top.first].fg.adj[a].push_back(pld(b,c));
				f[top.first].fg.rAdj[b].push_back(pld(a,c));
                                f[top.first].fg.fIn[b]+= c; 
				printf("pref Add F%ld (%ld,%ld)\n", 
					top.first,a,b);			     
	

			}
			
		}
	y=x;	
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
			build_funnel(G,f,*it);
			opt_funnel(G,f,*it);
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
