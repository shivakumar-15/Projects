#include<stdio.h>
#include<stdlib.h>
#include <string.h>

#include "buffer_mgr.h"
#include "dberror.h"
#include "storage_mgr.h"
#include "buffer_mgr_stat.h"
#include "pthread.h"
#include "record_mgr.h"

static char tmp1[1000];
// Linked list to help handle the various scan function transfer data between them
// change
typedef struct SNode
{
    RM_ScanHandle *scanHandle;
    int page;
    int slot;
    int totalrecordlength;
    int totalrecordsinpage;
    int totalnumPages;
    BM_PageHandle *ph;
    //Scan_Help *scanhelp;
    struct SNode *nextSNode;
} sNode,*sptr;

static sptr stptr=NULL;
static Schema Globalschema;

//Functions to handle the Linked list

bool insert_snode(sptr *startnode , RM_ScanHandle *scanHandle , sNode *node)
{
sptr prevNode;
sptr currNode;
//newNode=(sNode *)malloc(sizeof(sNode);

if(node!=NULL)
{
	node->scanHandle=scanHandle;
	node->nextSNode=NULL;
	
	prevNode=NULL;
	currNode=*startnode;

	while(currNode!=NULL)
	{
		prevNode=currNode;
		currNode=currNode->nextSNode;
	}
	if(prevNode==NULL){
	*startnode=node; }
	else {
	prevNode->nextSNode=node; }
	
	return TRUE;
}
else
{
	printf("The node has no memory allocated");
	return FALSE;
}
}

sNode *search_snode(sptr startnode , RM_ScanHandle *scanHandle)
{
    sptr prevnode;
    sptr currnode;

    prevnode=NULL;
    currnode=startnode;

    while(currnode!=NULL && currnode->scanHandle!=scanHandle)
    {
        prevnode=currnode;
        currnode=currnode->nextSNode;
    }

    return currnode;
}

bool delete_snode(sptr *startnode , RM_ScanHandle *scanHandle)
{
sptr tnode;
sptr prevnode;
sptr currnode;

prevnode=NULL;
currnode=*startnode;

while(currnode!=NULL && currnode->scanHandle!=scanHandle)
{
        prevnode=currnode;
        currnode=currnode->nextSNode;
}

if(currnode!=NULL)
{
	tnode=currnode;
	if(prevnode==NULL)
	{
		*startnode=currnode->nextSNode;
	}
	else
	{
		prevnode->nextSNode=currnode->nextSNode;
	}
	free(tnode);
	return TRUE;
}
else
{
	printf("The Node doesnt exist");
	return FALSE;
}
}


// table and manager
extern RC initRecordManager (void *mgmtData)
{
return RC_OK;
}


extern RC shutdownRecordManager ()
{
return RC_OK;
}

//works just change txt
extern RC createTable (char *name, Schema *schema)
{
Globalschema=*schema;//This is used as an cache for a active table instead of reading Schema every time from file.
char file[100]={'\0'};
int i,pos=0;
strcpy(file,name);
strcat(file,".txt");
createPageFile(file);
BM_PageHandle *pg=MAKE_PAGE_HANDLE();
BM_BufferPool *bm=MAKE_POOL();
initBufferPool(bm,file,1,RS_FIFO,NULL);
pinPage(bm,pg,0);
//have to do some changes here
for(i=0;i < schema->numAttr;i++)
{
	pos+=sprintf(pg->data+pos,"Numattr-%d,DataType[%d]-%d,Typelength[%d]=%d",schema->numAttr,i,schema->dataTypes[i],i,schema->typeLength[i]);//Write the schema by getting the offset.
}
markDirty(bm,pg);
unpinPage(bm,pg);
forceFlushPool(bm);
shutdownBufferPool(bm);
return RC_OK;
}

//doesnt work
extern RC openTable (RM_TableData *rel, char *name)
{
char file[100]={'\0'};
Schema *sc=(Schema *)malloc(sizeof(Schema));
*sc=Globalschema;
rel->schema=sc;
strcpy(file,name);
strcat(file,".txt");
BM_BufferPool *bm=MAKE_POOL();//We access the page file using buffer manager.
initBufferPool(bm,file,4,RS_FIFO,NULL);//Create a new buffer pool with FIFO logic.
rel->name=name;
rel->mgmtData=bm;
return RC_OK;
}


extern RC closeTable (RM_TableData *rel)
{
BM_BufferPool *bm=(BM_BufferPool *)rel->mgmtData;
shutdownBufferPool(bm);//Shutdown the pool associated with that table.
free(bm);
freeSchema(rel->schema);//Free up the schema.
return RC_OK;
}


extern RC deleteTable (char *name)
{
char file[100]={'\0'};
strcpy(file,name);
strcat(file,".txt");
destroyPageFile(file);
return RC_OK;
}


extern int getNumTuples (RM_TableData *rel)
{
BM_BufferPool *bm=(BM_BufferPool *)rel->mgmtData;
BM_PageHandle *ph=MAKE_PAGE_HANDLE();//Create a page handle for this scan alone.
SM_FileHandle *sh=(SM_FileHandle *)bm->mgmtData;
int i;
int nooftuples=0;
PageNumber pgno=1;
int pagelength;
    while(pgno < sh->totalNumPages)//Loop through all the page files.
    {
      pinPage(bm,ph,pgno);
      pagelength=strlen(ph->data);
      if(pagelength > 0)
      {
          for(i=0;i < PAGE_SIZE;i++)
          {
		if(ph->data[i]=='|')
		{
               		nooftuples=nooftuples+1;
		}
          }
      }
       unpinPage(bm,ph);
      pgno++;
  }
    free(ph);
    return nooftuples;
}


PageNumber getPageNo(RM_TableData *rel,BM_BufferPool *bufferPool,BM_PageHandle *pagehandle,int *currentslotid)
{
    PageNumber _pgno=1;
    int pagelength,totalrecordlength;
    SM_FileHandle *sh=(SM_FileHandle *)bufferPool->mgmtData;
    totalrecordlength=getRecordSize(rel->schema);
    //Scan through all the pages to find an empty slot.
    while(_pgno < sh->totalNumPages)
    {
      pinPage(bufferPool,pagehandle,_pgno);
      pagelength=strlen(pagehandle->data);
      if(PAGE_SIZE-pagelength > totalrecordlength)//If found empty slot. get the slot id.
      {
          *currentslotid=pagelength/totalrecordlength;
          unpinPage(bufferPool,pagehandle);
          break;
      }
       unpinPage(bufferPool,pagehandle);
      _pgno++;
  }
  if(*currentslotid==0)//If not slot id is found , mean all pages are full , append the page file and return that page number.
  {
      pinPage(bufferPool,pagehandle,_pgno + 1);
      unpinPage(bufferPool,pagehandle);
  }
  return _pgno;
}


// handling records in a table
extern RC insertRecord (RM_TableData *rel, Record *record)
{
BM_BufferPool *bm=(BM_BufferPool *)rel->mgmtData;
BM_PageHandle *ph=MAKE_PAGE_HANDLE();
int freepage=0;
PageNumber pno=getPageNo(rel,bm,ph,&freepage);
pinPage(bm,ph,pno);
char *tmp=NULL;
tmp=ph->data;
tmp=tmp+strlen(ph->data);
strcpy(tmp,record->data);
markDirty(bm,ph);
unpinPage(bm,ph);
RID rid;
rid.page=pno;
rid.slot=freepage;
record->id=rid;
free(ph);
return RC_OK;
}


extern RC deleteRecord (RM_TableData *rel, RID id)
{
BM_BufferPool *bm=(BM_BufferPool *)rel->mgmtData;
BM_PageHandle *ph=MAKE_PAGE_HANDLE();
int recsize=getRecordSize(rel->schema);
int frame=id.slot,i;
PageNumber pno=id.page;
char *data=NULL;
char *datatodelete=NULL;
if(pinPage(bm,ph,pno)==RC_OK)
{
	data=ph->data;
	datatodelete= data + recsize*frame;
	for(i=0;i<recsize;i++)
	{
		datatodelete[i]='#';
	}
	markDirty(bm,ph);
	unpinPage(bm,ph);
}
else
{
return RC_IM_KEY_NOT_FOUND;
}
free(ph);
return RC_OK;
}


extern RC updateRecord (RM_TableData *rel, Record *record)
{
BM_BufferPool *bm=(BM_BufferPool *)rel->mgmtData;
BM_PageHandle *ph=MAKE_PAGE_HANDLE();
int recsize=getRecordSize(rel->schema);
RID id=record->id;
int frame=id.slot;
PageNumber pno=id.page;
char *data=NULL;
char *datatoupdate=NULL;
if(pinPage(bm,ph,pno)==RC_OK)
{
	data=ph->data;
	datatoupdate= data + recsize*frame;
	strncpy(datatoupdate,record->data,recsize);
	markDirty(bm,ph);
	unpinPage(bm,ph);
}
else
{
return RC_IM_KEY_NOT_FOUND;
}
free(ph);
return RC_OK;
}


extern RC getRecord (RM_TableData *rel, RID id, Record *record)
{
BM_BufferPool *bm=(BM_BufferPool *)rel->mgmtData;
BM_PageHandle *ph=MAKE_PAGE_HANDLE();
int recsize=getRecordSize(rel->schema);
int frame=id.slot;
PageNumber pno=id.page;
char *data=NULL;
char *datatoupdate=NULL;
if(pinPage(bm,ph,pno)==RC_OK)
{
	data=ph->data;
	datatoupdate= data + recsize*frame;
	strncpy(record->data,datatoupdate,recsize);
	record->id=id;
	markDirty(bm,ph);
	unpinPage(bm,ph);
}
else
{
return RC_IM_KEY_NOT_FOUND;
}
free(ph);
return RC_OK;
}

// scans
extern RC startScan (RM_TableData *rel, RM_ScanHandle *scan, Expr *cond)
{
BM_BufferPool *bm=(BM_BufferPool *)rel->mgmtData;
BM_PageHandle *ph=MAKE_PAGE_HANDLE();
SM_FileHandle *fh=(SM_FileHandle *)bm->mgmtData;
sNode *sn=(sNode *)malloc(sizeof(sNode));
scan->rel=rel;
scan->mgmtData= cond;
//This is used to handle multiple scans for a same file where active scans are loaded in linked list.
sn->page=1;
sn->totalnumPages=fh->totalNumPages;
sn->totalrecordlength=getRecordSize(rel->schema);
sn->totalrecordsinpage=0;
sn->slot=1;
sn->ph=ph;
sn->scanHandle=scan;
insert_snode(&stptr,scan,sn);//Insert active scan to a linked list.
return RC_OK;
}


extern RC next (RM_ScanHandle *scan, Record *record)
{
int pagelength;
    Expr *_expr=(Expr *)scan->mgmtData,*secondaryexpr,*left,*right;
    Operator *scancriteria,*secondscancriteria;
    RM_TableData *_rel=scan->rel;
    sNode *sn=search_snode(stptr,scan);
    RID _id;
    Value **columnvalue=(Value **)malloc(sizeof(Value *));//Exact column value thats needs to be checked in expression.
    *columnvalue=NULL;
    bool matchfound=FALSE;

//We divide scans into two. One with expression and other NULL
    if(_expr==NULL)
    {
        //1.Return all the tuples.
        //2.Once all the tuples returned... return no more tuples.
      if(sn->page < sn->totalnumPages)//Scan through all the pages of the table.
      {
          pinPage(_rel->mgmtData,sn->ph,sn->page);
          pagelength=strlen(sn->ph->data);
          sn->totalrecordsinpage=pagelength/sn->totalrecordlength;
          if(sn->slot < sn->totalrecordsinpage)//scan through all the slots and get the record.
          {
              _id.page=sn->page;
              _id.slot=sn->slot;
              getRecord(_rel,_id,record);
              sn->slot++;
          }
          else
          {
              sn->page+=1;
              sn->slot=1;
          }
          unpinPage(_rel->mgmtData,sn->ph);
          free(columnvalue[0]);
          free(columnvalue);
          return RC_OK;
      }
      else
      {
          free(columnvalue[0]);
          free(columnvalue);
          return RC_RM_NO_MORE_TUPLES;//Once done with the scans.. returns no more tuples to indicate end of the scan.
      }
    }
    else
    {
        //1.return those tuples that satisfy the condition alone.
        //2. Once done return no more tuples.
    scancriteria=_expr->expr.op;//Get the main scan criteria.
    switch(scancriteria->type)
      {
      case OP_COMP_EQUAL://do the above operation for equal criteria.
        left=scancriteria->args[0];
        right=scancriteria->args[1];
        while(sn->page < sn->totalnumPages)
      {
          pinPage(_rel->mgmtData,sn->ph,sn->page);
          pagelength=strlen(sn->ph->data);
          sn->totalrecordsinpage=pagelength/sn->totalrecordlength;
          while(sn->slot < sn->totalrecordsinpage)
          {
              _id.page=sn->page;
              _id.slot=sn->slot;
              getRecord(_rel,_id,record);
              getAttr(record,_rel->schema,right->expr.attrRef,columnvalue);
              if(_rel->schema->dataTypes[right->expr.attrRef]==DT_INT){
              if(columnvalue[0]->v.intV == left->expr.cons->v.intV)//Check whether the scan condition and column value from page are equal for integers.
              {
                 sn->slot++;
                 unpinPage(_rel->mgmtData,sn->ph);
                 matchfound=TRUE;//Indicate that a match has been found.
                 break;
              }
              }
              else if(_rel->schema->dataTypes[right->expr.attrRef]==DT_STRING)//Check whether the scan condition and column value from page are equal for integers.
                {
                    if(strcmp(columnvalue[0]->v.stringV , left->expr.cons->v.stringV)==0)
                {
                 sn->slot++;
                 unpinPage(_rel->mgmtData,sn->ph);
                 matchfound=TRUE;
                 break;
                }
                }
                 else if(_rel->schema->dataTypes[right->expr.attrRef]==DT_FLOAT)//Check whether the scan condition and column value from page are equal for float values.
                {
                    if(columnvalue[0]->v.floatV == left->expr.cons->v.floatV)
                {
                 sn->slot++;
                 unpinPage(_rel->mgmtData,sn->ph);
                 matchfound=TRUE;
                 break;
                }
                }

               sn->slot++;
           }
          if(matchfound==TRUE)
            break;
          else
          {
           sn->page+=1;
           sn->slot=1;
           unpinPage(_rel->mgmtData,sn->ph);
          }
      }
      break;
      case OP_COMP_SMALLER:
        left=scancriteria->args[0];
        right=scancriteria->args[1];
        while(sn->page < sn->totalnumPages)
      {
          pinPage(_rel->mgmtData,sn->ph,sn->page);
          pagelength=strlen(sn->ph->data);
          sn->totalrecordsinpage=pagelength/sn->totalrecordlength;
          while(sn->slot < sn->totalrecordsinpage)
          {
              _id.page=sn->page;
              _id.slot=sn->slot;
              getRecord(_rel,_id,record);
              getAttr(record,_rel->schema,right->expr.attrRef,columnvalue);
              if(_rel->schema->dataTypes[right->expr.attrRef]==DT_INT){
              if(columnvalue[0]->v.intV < left->expr.cons->v.intV)
              {
                 sn->slot++;
                 unpinPage(_rel->mgmtData,sn->ph);
                 matchfound=TRUE;
                 break;
              }
              }
              sn->slot++;
          }
          if(matchfound==TRUE)
            break;
          else
          {
           sn->page+=1;//Increment the page.
           sn->slot=1;//Reset the slot.
           unpinPage(_rel->mgmtData,sn->ph);
          }
      }
      break;
      case OP_BOOL_NOT://seperate case for boolean NOT !
          secondaryexpr=_expr->expr.op->args[0];
          secondscancriteria=secondaryexpr->expr.op;
          left=secondscancriteria->args[1];
          right=secondscancriteria->args[0];

        switch(secondscancriteria->type)

        {
        case OP_COMP_SMALLER:
      while(sn->page < sn->totalnumPages)
      {
          pinPage(_rel->mgmtData,sn->ph,sn->page);
          pagelength=strlen(sn->ph->data);
          sn->totalrecordsinpage=pagelength/sn->totalrecordlength;
          while(sn->slot < sn->totalrecordsinpage)
          {
              _id.page=sn->page;
              _id.slot=sn->slot;
              getRecord(_rel,_id,record);
             getAttr(record,_rel->schema,right->expr.attrRef,columnvalue);
              if(_rel->schema->dataTypes[right->expr.attrRef]==DT_INT){
              if(columnvalue[0]->v.intV > left->expr.cons->v.intV)
              {
                 sn->slot++;
                 unpinPage(_rel->mgmtData,sn->ph);
                 matchfound=TRUE;
                 break;
              }
              }
               sn->slot++;
            }
          if(matchfound==TRUE)
            break;
          else
          {
           sn->page+=1;
           sn->slot=1;
           unpinPage(_rel->mgmtData,sn->ph);
          }
      }
      break;

      }
      break;

      }
      free(*columnvalue);//free the column value we created.
      free(columnvalue);////free the column value we created.
      if(matchfound==TRUE)
return RC_OK;//end the scan once the match is found.
else
    return RC_RM_NO_MORE_TUPLES;
 }
}


extern RC closeScan (RM_ScanHandle *scan)
{
//sNode *sn=search_snode(stptr,scan);
//free(sn);
delete_snode(&stptr,scan);
return RC_OK;
}

// dealing with schemas
extern int getRecordSize (Schema *schema)
{
int num=schema->numAttr;
DataType *dts=schema->dataTypes;
int *len=schema->typeLength;
int size=0,i;
for(i=0;i<num;i++)
{
	DataType dt=*(dts + i);
	if(dt==DT_INT)
	{
	size+=sizeof(int);
	}
	else if(dt==DT_FLOAT)
	{
	size+=sizeof(float);
	}
	else if(dt==DT_BOOL)
	{
	size+=sizeof(bool);
	}
	else if(dt==DT_STRING)
	{
	size+=len[i];
	}

}
return size+num;
}


extern Schema *createSchema (int numAttr, char **attrNames, DataType *dataTypes, int *typeLength, int keySize, int *keys)
{
Schema *schema = (Schema*) malloc(sizeof(Schema));
schema->numAttr = numAttr;
schema->attrNames = attrNames;
schema->dataTypes = dataTypes;
schema->typeLength = typeLength;
schema->keySize = keySize;
schema->keyAttrs = keys; 
return schema;
}


extern RC freeSchema (Schema *schema)
{
free(schema);
return RC_OK;
}

// dealing with records and attribute values
extern RC createRecord (Record **record, Schema *schema)
{
int num=schema->numAttr;
DataType *dts=schema->dataTypes;
int *len=schema->typeLength;
int i,mem=0;
char *data;
// a little change here to get record size
mem=getRecordSize(schema);
data=(char*)malloc(mem);
for(i=0;i<num;i++)
{
data[i]='\0';
}
*record=(Record *)malloc(sizeof(Record));
record[0]->data=data;
return RC_OK;

}

extern RC freeRecord (Record *record)
{
free(record);//free record pointer.
return RC_OK;
}

//doesnt work
RC getAttr(Record *record, Schema *schema, int attrNum, Value **value) 
{
int *len = schema->typeLength;
int num = schema->numAttr;
DataType *dts = schema->dataTypes;
int addr = 1,i;
char *data = record->data;
Value *val = (Value*) malloc(sizeof(Value));
tmp1[100]='\0';
char *tmp=NULL;//Used to substring the data from record and convert it to required datatype.

if (attrNum < num) 
{
	//Loop through the whole tuple to get the required addr
	for (i = 0; i < attrNum; i++) 
	{
	if (dts[i] == DT_INT) 
	{
		addr += sizeof(int);
	} else if (dts[i]== DT_FLOAT) {
		addr += sizeof(float);
	} else if (dts[i]== DT_BOOL) {
		addr += sizeof(bool);
	} else if (dts[i]== DT_STRING) { /*In case it is a String, the size will be equal to the corresponding type length*/
		addr += len[i];
	}
	}
addr+=attrNum;
int attrsize = 0;
int dt = *(dts + i);/*The value of i would have incremented */
/*Set the datatype of Value*/		
if (dt == DT_INT) 
{
	val->dt = DT_INT;
	attrsize += sizeof(int);
	tmp=malloc(attrsize+1);
} 
else if (dt == DT_FLOAT) 
{
	val->dt = DT_FLOAT;
	attrsize += sizeof(float);
	tmp=malloc(attrsize+1);
} 
else if (dt == DT_BOOL) 
{
	val->dt = DT_BOOL;
	attrsize += sizeof(bool);
	tmp=malloc(attrsize+1);
} 
else if (dt == DT_STRING) 
{ /*In case it is a String, the size will be equal to the corresponding type length*/
	val->dt = DT_STRING;
	attrsize += *(len + i);
	tmp=malloc(attrsize+1);
	for(i=0;i <= attrsize ; i++)
        {
        	tmp[i]='\0';
        }
}

strncpy(tmp, data + addr, attrsize); //Check if addr has to be divided by, say 2, because addr will be in bytes and you might want to get in chars
tmp[attrsize]='\0';
/*Set the data element of Value*/
if (val->dt == DT_INT) {
	val->v.intV = atoi(tmp);
} 
else if (val->dt == DT_FLOAT) 
{
	val->v.floatV = (float) *tmp;
} 
else if (val->dt == DT_BOOL) 
{
	val->v.boolV = (bool) *tmp;
} 
else if (val->dt == DT_STRING) 
{
	for(i=0;i < attrsize;i++)
        {
	        tmp1[i]=tmp[i];
        }
	val->v.stringV=tmp1;
}
value[0]=val;
free(tmp);
return RC_OK;
}
/*If attrNum is greater than numAttr - Set the error message*/
RC_message = "attrNum is greater than the available number of attributes";
return RC_RM_NO_MORE_TUPLES;

}


extern RC setAttr (Record *record, Schema *schema, int attrNum, Value *value)
{
int *len=schema->typeLength;
int num=schema->numAttr;
DataType *dts=schema->dataTypes;
int tmp;
int addr=1;
if(attrNum<num)
{
int i=0,j;
for(i=0;i<attrNum;i++)
{
	if (dts[i] == DT_INT) {
	addr += sizeof(int);
	} else if (dts[i]== DT_FLOAT) {
	addr += sizeof(float);
	} else if (dts[i]== DT_BOOL) {
	addr += sizeof(bool);
	} else if (dts[i]== DT_STRING) {
	addr += len[i];
	}
}
addr+=attrNum;

char *setaddr;
if(attrNum==0)
{
	setaddr =record->data ;
	setaddr[0]='|';//Used to sepearate different tuples in a page file.
	setaddr++;
}
else
{
	setaddr=record->data+addr;
	(setaddr-1)[0]=',';//Comma seperator for records in a tuple.
}
if (value->dt == DT_INT) 
{
	sprintf(setaddr,"%d",value->v.intV);
	while(strlen(setaddr)!=sizeof(int))
        {
	        strcat(setaddr,"0");
        }
//format integer to string
	for (i=0,j=strlen(setaddr)-1 ; i < j;i++,j--)
	{
		tmp=setaddr[i];
        	setaddr[i]=setaddr[j];
        	setaddr[j]=tmp;
    	}

} 
else if (value->dt == DT_FLOAT) 
{
	sprintf(setaddr,"%f",value->v.floatV);
	while(strlen(setaddr)!=sizeof(float))
        {
	        strcat(setaddr,"0");
        }
//format float to string
	for (i=0,j=strlen(setaddr)-1 ; i < j;i++,j--)
	{
        	tmp=setaddr[i];
        	setaddr[i]=setaddr[j];
        	setaddr[j]=tmp;
	}
} 
else if (value->dt == DT_BOOL) 
{
	sprintf(setaddr,"%i",value->v.boolV);//Convert bool to string
} 
else if (value->dt == DT_STRING) 
{ //In case it is a String, the size will be equal to the corresponding type length
	sprintf(setaddr,"%s",value->v.stringV);
}
return RC_OK;
}
else
{
RC_message = "attrNum is greater than the available number of Attributes";
return RC_RM_NO_MORE_TUPLES;
}
}



