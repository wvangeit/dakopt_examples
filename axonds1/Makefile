clean: clean_nb clean_ms
clean_ms:
	@rm -rf map-service
clean_nb:                                                                                                                                                                                                                         
	@rm -rf notebook/inputs                                                                                                                                                                                                        
	@rm -rf notebook/outputs
clean_dataset:
	@rm -rf notebook/r20211130-ivadomed_dataset.zip	
	@rm -rf notebook/example_r20211130-ivadomed_dataset
	@rm -rf notebook/data_axondeepseg_sem-r20211130
notebook: osparc_whl
	@cd notebook && \
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
	pip install -q /home/vangeit/src/osparc-studymap/docker_scripts/*.whl
dataset: clean_dataset
	cd notebook && \
	   wget -q https://github.com/axondeepseg/data_axondeepseg_sem/archive/r20211130.zip -O r20211130.zip && \
	   unzip -q r20211130.zip
	mkdir notebook/example_r20211130-ivadomed_dataset
	cd notebook/example_r20211130-ivadomed_dataset && \
		cp ../data_axondeepseg_sem-r20211130/LICENSE . && \
		find ../data_axondeepseg_sem-r20211130 -wholename '*_SEM.png' -exec cp {} . \; && \
		find ../data_axondeepseg_sem-r20211130 -wholename '*_SEM.json' -exec cp {} . \; && \
		cp sub-rat3_SEM.json sub-rat3_sample-data9_SEM.json && \
		cp sub-rat3_SEM.json sub-rat3_sample-data10_SEM.json && \
		cp sub-rat3_SEM.json sub-rat3_sample-data11_SEM.json && \
	    rm sub-rat3_SEM.json && \
		rm sub-rat6_sample-data15_SEM.*
	cd notebook && \
		rm -rf data_axondeepseg_sem-r20211130
map-service: link_io osparc_whl
	@mkdir -p map-service	
	@cp test_data/key_values.json map-service/inputs                                                                                                                                                                               
	@cd map-service && \
	  wget -q https://raw.githubusercontent.com/wvangeit/osparc-studymap/master/docker_scripts/map.py && \
	    OSPARC_API_KEY=`cat ../osparc_api_key.txt` \
	      OSPARC_API_SECRET=`cat ../osparc_api_secret.txt` \
	      DY_SIDECAR_PATH_INPUTS=./inputs \
          DY_SIDECAR_PATH_OUTPUTS=./outputs \
	      python map.py        	
start: notebook map-service
