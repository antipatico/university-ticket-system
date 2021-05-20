const OrganizationsApp = {
    delimiters: ['$%', '%$'],
    data() {
        return {
            organizations: null,
            administeredOrganizations: null,
            joinedOrganizations: null,
            userToRemove: null,
            modalOrganization: null,
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
                $("#modalRemoveUser").modal("hide");
            }
        },
        addUserModal(organization) {
            this.modalOrganization = organization;
            $("#modalAddUser").modal("show");
        }
    }
}
const app = Vue.createApp(OrganizationsApp).mount("#organizationsApp");