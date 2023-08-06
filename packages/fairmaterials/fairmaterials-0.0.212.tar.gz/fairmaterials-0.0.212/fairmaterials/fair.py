class fairjson:
    from pandas.io.json import json_normalize
    import pandas as pd
    import json,os,copy
    from IPython.display import display
    # %%
    def setValue(self,key,value):
        '''
        Set value based on key name. 
        '''
        if key in self.all_name:
            self.dealWithInput(key+'>'+value)
        else:
            print('Can not find key:',key)    

    def searchKey(self,key)->str:
        '''
        Search value based on key name. 
        '''
        return self.dealWithInput('?'+key)

    def importCsv(self,filename):
        '''
        Import data from csv file as input for json. 
        '''
        csvf=pd.read_csv(filename)
        for i in csvf.columns:
            if i in self.all_name.keys():
                self.editDFs(i,str(csvf.loc[0,i]))
            else:
                print('found a data not in the defined names',[i,str(csvf.loc[0,i])])

    def editDFs(self,inname:str,inValue:str):
        if inname in self.name_sch.keys():
            for i in range(len(self.name_sch[inname])):
                chunkname=self.name_sch[inname][i][0]
                colname=self.name_sch[inname][i][1]
                for j in range(len(self.chunks_list)):
                    if inname in self.name_sch.keys():
                        if self.chunks_list[j]==chunkname:
                            self.Working_on_sch[j].loc['SchemaMetadata',colname]=inValue
        if inname in self.name_add.keys():
            for i in range(len(self.name_add[inname])):
                chunkname=self.name_add[inname][i][0]
                indexname=self.name_add[inname][i][1]
                for j in range(len(self.chunks_list)):
                    if self.chunks_list[j]==chunkname and indexname in self.Working_on_add[j].index:
                        self.Working_on_add[j].loc[indexname,'value']=inValue

    def getValue(self,inname:str):
        if inname in self.name_sch.keys():
            for i in range(len(self.name_sch[inname])):
                chunkname=self.name_sch[inname][i][0]
                colname=self.name_sch[inname][i][1]
                for j in range(len(self.chunks_list)):
                    if inname in self.name_sch.keys():
                        if self.chunks_list[j]==chunkname:
                            return self.Working_on_sch[j].loc['SchemaMetadata',colname]
        if inname in self.name_add.keys():
            for i in range(len(self.name_add[inname])):
                chunkname=self.name_add[inname][i][0]
                indexname=self.name_add[inname][i][1]
                for j in range(len(self.chunks_list)):
                    if self.chunks_list[j]==chunkname and indexname in self.Working_on_add[j].index:
                        return self.Working_on_add[j].loc[indexname,'value']

    def display_current_JSONDF(self):
        '''
        Print current data in shell. 
        '''
        for i in range(len(self.Working_on_sch)):
            display('Chunk name: '+list(self.Working_on_DF.index)[i])
            display(self.Working_on_sch[i].drop('@type',axis=1))
            display(self.Working_on_add[i].drop('@type',axis=1))
            display('----------------------------------------------------------------')

    def save_to_json(self,outputname):
        '''
        Output current data as json file. 
        '''
        def buildSchPart(inDF:pd.DataFrame)->str:
            schpart=inDF.to_json(orient='index')
            parsed = json.loads(schpart)
            json_string = json.dumps(parsed)
            return json_string[1:-1]

        def buildAddJsonPart(inDF)->str:
            json_str = inDF.to_json(orient='index')
            parsed = json.loads(json_str)
            json_string = json.dumps(parsed) 
            json_string = "\""+"additionalProperty:"+"\": "+json_string
            return json_string

        def buildDifferentMetaParts(nameList,eachLisfWithsch_add)->str:
            metas_json=""
            for single_name in nameList:
                metas_json=metas_json+"\""+single_name+"\": {"
                metas_json=metas_json+eachLisfWithsch_add[nameList.index(single_name)]+"},"
            return metas_json[:-1]
      
        def addTopestLevel(topName,eachMetaChunk)->str: 
            top_json="{"+"\""+topName+"\": {"
            top_json=top_json+eachMetaChunk+"}}"
            return top_json
         
        Chunks=[]
        for i in range(len(self.chunks_list)):
            smallChunk=buildSchPart(self.Working_on_sch[i])+','+buildAddJsonPart(self.Working_on_add[i]) 
            Chunks.append(smallChunk)
        final_json=[addTopestLevel(self.topest_name,buildDifferentMetaParts(self.chunks_list,Chunks))]
        with open(outputname, 'w') as f:    
            for item in final_json:                  
                f.write("%s\n" % item)
    
    def getAllNames(self):
        '''
        return the names of all keys
        '''
        return list(self.all_name.keys())

    def dealWithInput(self,inStr:str):
        '''
        A alternative input based on string command.
        '''
        if "?" == inStr[0]:
            if inStr[1:] in self.all_name.keys():
                return self.all_name[inStr[1:]]
            else:
                return 'Can not find the description of the name'
        if ">" in inStr:
            namePart=inStr[0:inStr.index(">")]
            valuepart=inStr[inStr.index(">")+1:]
            if namePart in self.all_name.keys():
                self.editDFs(namePart, valuepart)
                return 'Changed value'
            else:
                return 'Can not find the input name'
        if inStr=='!save':
            self.save_to_json()
            return 'Saved to json file!'
        if inStr=='!import':
            csvname=input('Input the csv file name')
            csvf=pd.read_csv(csvname)
            for i in csvf.columns:
                if i in self.all_name.keys():
                    self.editDFs(i,str(csvf.loc[0,i]))
                else:
                    print('found a data not in the defined names',[i,str(csvf.loc[0,i])])


    def __init__(self, name):
        self.temName=name
        self.temDF=pd.read_json(self.temName,orient='columns')
        self.Working_on_DF=copy.deepcopy(self.temDF)
        self.topest_name=self.Working_on_DF.columns[0]
        self.chunks_list=list(self.Working_on_DF.index)    
        self.Working_on_sch=[]
        self.Working_on_add=[]
        for s in self.chunks_list:
            self.Working_on_sch.append(pd.DataFrame(self.Working_on_DF.loc[s,self.topest_name]['SchemaMetadata'],index=['SchemaMetadata']))
            self.Working_on_add.append(pd.DataFrame(self.Working_on_DF.loc[s,self.topest_name]['additionalProperty']).T)
            #find name hidden in schema part
        self.name_sch={}
        self.name_add={}
        self.all_name={}
        for i in range(len(self.chunks_list)):
            s_sch=self.Working_on_sch[i]
            for column in s_sch.columns:
                if "$" in s_sch.loc['SchemaMetadata',column]:
                    fullStr=s_sch.loc['SchemaMetadata',column]          
                    name_str=fullStr[fullStr.index('$')+1:fullStr.index('>')]
                    if name_str not in self.name_sch:
                        self.name_sch[name_str]=[[self.chunks_list[i],column]]
                    else:
                        self.name_sch[name_str].append([self.chunks_list[i],column])
                    if name_str not in self.all_name.keys():
                        self.all_name[name_str]=s_sch.loc['SchemaMetadata','description']+': '+column
                    else:
                        print('WARNING: Duplicate name:',name_str,'with description: ',s_sch.loc['SchemaMetadata','description'])
                        self.all_name[name_str]=self.all_name[name_str]+', '+s_sch.loc['SchemaMetadata','description']+': '+column

        for i in range(len(self.chunks_list)):
            s_app=self.Working_on_add[i]
            for j in s_app.index:
                if 'value' in s_app.columns:
                    if "$" in s_app.loc[j,'value']:
                        fullStr=s_app.loc[j,'value']
                        name_str=fullStr[fullStr.index('$')+1:fullStr.index('>')]
                        if name_str not in self.all_name.keys():
                            self.all_name[name_str]=s_app.loc[j,'description']
                            if name_str not in self.name_add:
                                self.name_add[name_str]=[[self.chunks_list[i],j]]
                            else:
                                self.name_add[name_str].append([self.chunks_list[i],j])
                        else:
                            print('WARNING: Duplicate name:',name_str,'with description: ',s_app.loc[j,'description'])
                            self.all_name[name_str]=self.all_name[name_str]+', '+s_app.loc[j,'description']
                            if name_str not in self.name_add:
                                self.name_add[name_str]=[[self.chunks_list[i]]]
                            else:
                                self.name_add[name_str].append([self.chunks_list[i],j])
    
    def generate_group_input_csv(self,number_of_json_files:int):
        '''
        Generate a blank CSV file with name "group_input.csv" for group input
        '''  
        myheader=['key names:']
        description_line=['description:']
        myheader.extend(list(self.all_name.keys()))
        outputCSV=pd.DataFrame(columns=myheader)
        for i in self.all_name.keys():
            description_line.append(self.all_name[i])
        outputCSV.loc[len(outputCSV.index)] = description_line
        for i in range(number_of_json_files):
            outputCSV.loc[len(outputCSV.index),'key names:']='default'+str(i+1)+'.json'
        outputCSV.to_csv('group_input.csv',index=None,encoding='UTF-8')
        print('Generated the CSV file!')

    def convert_group_input_csv_to_json_files(self,csvname:str):
        '''
        Directly convert a group input CSV file to multiple json files
        '''
        csv_df=pd.read_csv(csvname)
        display(csv_df)
        display(list(csv_df.columns))
        for i in csv_df.index:
            if csv_df.loc[i,'key names:']!='description:':
                for j in list(csv_df.columns):
                    if j!='key names:':
                        if str(csv_df.loc[i,j])!= "nan":
                            self.setValue(str(j),str(csv_df.loc[i,j]))
                        else:
                            self.setValue(str(j),'Null')
                self.save_to_json(str(csv_df.loc[i,'key names:']))
                print('save as',str(csv_df.loc[i,'key names:']))