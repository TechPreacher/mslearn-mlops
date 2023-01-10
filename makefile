job: file=job.yml 
job: computeInput?=$(COMPUTE)
job: local?=false
job:
    @if [ "$(local)" =  true ] ; then { \
        if [ -d "data/diabetes-dev-data/2" ] ; then { \
            echo "directory is already downloaded"; \
        } else { \
            python src/download.py; \
        } fi ;\
        kubectl apply -f kubernetes/volumemount.yml; \
        az ml job create -f $(CODE_PATH)/$(file) --resource-group $(RESOURCE_GROUP) --workspace-name $(WORKSPACE) --set compute=$(computeInput) --set inputs.training_data="/mnt/nfs" ; \
    } else { \
        az ml job create -f $(CODE_PATH)/$(file) \
            --resource-group $(RESOURCE_GROUP) --workspace-name $(WORKSPACE) --set compute=$(computeInput) ; \
    } fi
    @echo "";
