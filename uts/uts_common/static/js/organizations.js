const OrganizationsApp = {
    delimiters: ['$%', '%$'],
    data() {
        return {
            organizations: null,
            administeredOrganizations: null,
            joinedOrganizations: null,
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
        }
    }
}
const app = Vue.createApp(OrganizationsApp).mount("#organizationsApp");