const FileSelector = {
    props: {
        multiFile: Boolean,
    },
    data() {
        return {
            file: null,
            uploadedFiles: {},
            error: null,
        };
    },
    methods: {
        handleFileUpload() {
            this.error = null;
            if(this.uploadedFiles.length > 0 && !this.multiFile) {
                this.error = "puoi allegare soltanto un singolo file";
                return;
            }
            this.file = this.$refs.file.files[0];
            if(this.file.size > MAX_FILE_SIZE) {
                this.error = "file troppo grande (dimensioni massime: 10 MB)";
                return;
            }
            let formData = new FormData();
            formData.append('file', this.file);
            $.ajax(API_FILE_UPLOAD_URL, {
                type: "POST",
                data: formData,
                contentType: false,
                processData: false,
                headers: {'X-CSRFToken': csrftoken},
            })
             .done((data) => {
                 console.log("Success");
                 console.log(data);
                 this.uploadedFiles[data.id] = data;
             })
             .fail((response) => {
                 console.log("Failure");
                 console.log(response);
             });
        },
        deleteFile(id) {
            if(this.uploadedFiles[id] == null) {
                console.error("can't delete a non-existing file.");
                return;
            }
            let f = this.uploadedFiles[id];
            QACommon.httpJSON("DELETE", API_FILE_UPLOAD_URL + f.id + "/", {},
                () =>{
                delete this.uploadedFiles[id];
            });
        },
    },
    template: `
    <div class="m-2">
      <div class="alert alert-danger mb-3" role="alert" v-if="error != null">
        <strong>Errore:</strong> {{ error }}
      </div>
      <input type="file" id="fileSelector" ref="file" v-on:change="handleFileUpload()" style="display:none">
      <div class="row">
        <div class="col-lg-12 mb-3" v-for="attachment in this.uploadedFiles">
          <div class="row">
              <div class="col-11"><strong><a :href="attachment.file" target="_blank">{{ attachment.name }}</a></strong></div>
              <div class="col-1 click"><i class="bi bi-x-circle text-danger" v-on:click="deleteFile(attachment.id)"></i></div>
          </div>
        </div>
      </div>
      <button class="btn btn-primary" v-on:click="$refs.file.click()" v-if="this.uploadedFiles.length < 1 || this.multiFile">Aggiungi un allegato</button>
    </div>`,
}