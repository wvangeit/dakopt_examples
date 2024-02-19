clean: clean_nb
clean_nb:                                                                                                                                                                                                                         
	@rm -rf notebook/inputs                                                                                                                                                                                                        
	@rm -rf notebook/outputs  
notebook: clean
	cd notebook && \
	DY_SIDECAR_PATH_INPUTS=./inputs \
	   DY_SIDECAR_PATH_OUTPUTS=./outputs \
	   OSPARC_API_KEY=`cat ../osparc_api_key.txt` \
	   OSPARC_API_SECRET=`cat ../osparc_api_secret.txt` \
	   jupyter nbconvert --execute --to notebook --inplace AxonDeepSeg.ipynb
jupyter:
	@mkdir -p notebook/outputs/output_1
	@mkdir -p notebook/inputs/input_1  
	cd notebook && \
	   DY_SIDECAR_PATH_INPUTS=./inputs \
	   DY_SIDECAR_PATH_OUTPUTS=./outputs \
	   OSPARC_API_KEY=`cat ../osparc_api_key.txt` \
	   OSPARC_API_SECRET=`cat ../osparc_api_secret.txt` \
	   jupyter notebook --no-browser --ip=0.0.0.0 --NotebookApp.token='hello' 	
start: notebook
