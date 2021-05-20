const OrganizationsApp = {
    delimiters: ['$%', '%$'],
    data() {
        return {
            organizations: null,
            administeredOrganizations: null,
            joinedOrganizations: null,
            modalOrganization: null,
            userToRemove: null,
            newUserEmail: null,
            addUserError: null,
        };
    },
    computed: {
        QACommon() { return QACommon}
    },
    created() {
        $("#organizationsApp").show();
    },
    mounted() {
        this.organizationsTimer = QACommon.interval(this.getOrganizations, 5 * 60 * 1000);
    },
    methods: {
        getOrganizations() {
            $.getJSON(API_ORGANIZATIONS_URL, this.postProcessOrganizations);
        },
        postProcessOrganizations(data) {
            this.organizations = data;
            this.administeredOrganizations = data.filter(org => org.administered);
            this.joinedOrganizations = data.filter(org => !org.administered);
        },
        confirmRemoveUser(user, organization) {
            this.userToRemove = user;
            this.modalOrganization = organization;
            $("#modalRemoveUser").modal("show");
        },
        removeUser() {
            if (this.userToRemove != null && this.modalOrganization != null) {
                let data = {
                    "delete_user_email": this.userToRemove.email
                }
                QACommon.httpJSON(
                    "DELETE",
                    API_ORGANIZATIONS_URL + this.modalOrganization.id + "/",
                        data,
                    () => {
                        $("#modalRemoveUser").modal("hide");
                        this.getOrganizations();
                    });
            }
        },
        addUserModal(organization) {
            this.addUserError = null;
            this.modalOrganization = organization;
            $("#modalAddUser").modal("show");

        },
        addUser() {
            this.addUserError = null;
            let data = {
                "new_user_email": this.newUserEmail
            }
            QACommon.httpJSON(
                    "PATCH",
                    API_ORGANIZATIONS_URL + this.modalOrganization.id + "/",
                        data,
                    () => {
                        $("#modalAddUser").modal("hide");
                        this.getOrganizations();
                        this.newUserEmail = null;
                    },
                    () => {
                        this.addUserError = true;
                    });
        }
    }
}
const app = Vue.createApp(OrganizationsApp).mount("#organizationsApp");