clean: clean_nb clean_ms
clean_ms:
	@rm -rf map-service
clean_nb:                                                                                                                                                                                                                         
	@rm -rf notebook/inputs                                                                                                                                                                                                        
	@rm -rf notebook/outputs  
notebook: osparc_whl
	cd notebook && \
	DY_SIDECAR_PATH_INPUTS=./inputs \
	   DY_SIDECAR_PATH_OUTPUTS=./outputs \
	   OSPARC_API_KEY=`cat ../osparc_api_key.txt` \
	   OSPARC_API_SECRET=`cat ../osparc_api_secret.txt` \
	   jupyter nbconvert --execute --to notebook --inplace AxonDeepSeg.ipynb
link_io: clean                                                                                                                                                                                                                     
	@mkdir -p notebook/outputs/output_1                                                                                                                                                                                            
	@mkdir -p notebook/inputs                                                                                                                                                                                                      
	@mkdir -p map-service/outputs/output_1                                                                                                                                                                                         
	@mkdir -p map-service/inputs                                                                                                                                                                                                   
	@ln -rs notebook/outputs/output_1 map-service/inputs/input_2                                                                                                                                                               
	@ln -rs map-service/outputs/output_1 notebook/inputs/input_1   
jupyter:
	@mkdir -p notebook/outputs/output_1
	@mkdir -p notebook/inputs/input_1  
	cd notebook && \
	   DY_SIDECAR_PATH_INPUTS=./inputs \
	   DY_SIDECAR_PATH_OUTPUTS=./outputs \
	   OSPARC_API_KEY=`cat ../osparc_api_key.txt` \
	   OSPARC_API_SECRET=`cat ../osparc_api_secret.txt` \
	   jupyter notebook --no-browser --ip=0.0.0.0 --NotebookApp.token='hello'
osparc_whl:
	pip install /home/vangeit/src/osparc-studymap/docker_scripts/*.whl 
map-service: link_io osparc_whl
	@mkdir -p map-service	
	@cp test_data/key_values.json map-service/inputs                                                                                                                                                                               
	cd map-service && \
	  wget -q https://raw.githubusercontent.com/wvangeit/osparc-studymap/master/docker_scripts/map.py && \
	    OSPARC_API_KEY=`cat ../osparc_api_key.txt` \
	      OSPARC_API_SECRET=`cat ../osparc_api_secret.txt` \
	      DY_SIDECAR_PATH_INPUTS=./inputs \
          DY_SIDECAR_PATH_OUTPUTS=./outputs \
	      python map.py        	
start: notebook map-service
