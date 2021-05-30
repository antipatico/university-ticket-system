const TicketsApp = {
    delimiters: ['$%', '%$'],
    components: {
        'file-selector': FileSelector,
    },
    data() {
        return {
            ticket: null,
            action: "NONE",
            info: null,
            duplicationUrl: null,
            newOwnerEmail: null,
            error: null,
            success: false,
            attachments: {},
            scheduled: false,
            scheduledDate: null,
            scheduledTime: null,
        }
    },
    mounted() {
        this.ticketDetailTimer = QACommon.interval(this.getTicketDetail, 10 * 1000);
    },
    created() {
        $("#ticketsApp").show();
    },
    computed: {
        TICKET_DETAILS_URL() { return TICKET_DETAILS_URL },
        QACommon() { return QACommon}
    },
    methods: {
        getTicketDetail() {
            $.getJSON(API_TICKETS_URL + TICKET_ID + "/", this.postProcessTicket);
        },

        postProcessTicket(data) {
            let owner = data.owner;
            data.events.forEach((e) => {
                if(e.status === "ESCALATION") {
                    e.newOwner = owner;
                    owner = e.owner;
                }
            });
            this.ticket = data;
        },
        toggleSubscription() {
            let data = {is_subscribed: !this.ticket.is_subscribed};
            QACommon.httpJSON("PATCH", API_TICKETS_URL + TICKET_ID + "/", data, this.postProcessTicket);
        },
        onAttachmentsChange(attachments) {
            this.attachments = attachments;
        },
        actionButtonClick() {
            this.success = false;
            this.error = null;

            let data = {
                "ticket_id": TICKET_ID,
                "status": this.action,
                "info": this.info,
                "attachments": this.attachments,
            }
            if(this.action === "NONE") {
                this.error = "perfavore seleziona un'azione";
                return;
            }
            if(this.action === "DUPLICATE") {
                if (this.duplicationUrl === null) {
                    this.error = "perfavore inserisci un URL";
                    return;
                }
                let match = this.duplicationUrl.match(/\/([0-9]+)$/);
                if (!match) {
                    this.error = "URL non valido";
                    return;
                }
                data["duplicate_id"] = parseInt(match[1]);
                delete data["info"];
            }

            if(this.action === "ESCALATION") {
                if(this.newOwnerEmail.length < 1) {
                    this.error = "perfavore inserisci l'email del nuovo proprietario";
                    return;
                }
                data["new_owner_email"] = this.newOwnerEmail;
                delete data["info"];
            }

            if(this.scheduled) {
                if(this.scheduledDate == null || this.scheduledTime == null) {
                    this.error ="perfavore seleziona data e ora";
                    return;
                }
                let dateTime = new Date(this.scheduledDate+" "+this.scheduledTime);
                if(dateTime < Date.now()) {
                    this.error = "perfavore seleziona una data futura";
                    return;
                }
                data["schedule_datetime"] = dateTime;
            }

            QACommon.httpJSON("POST", API_TICKET_EVENTS_URL, data,
                (data) => {
                    this.action = "NONE";
                    this.info = null;
                    this.duplicationUrl = null;
                    this.newOwnerEmail = null;
                    this.success = true;
                    this.attachments = [];
                    this.scheduled = false;
                    this.scheduledTime = null;
                    this.scheduledDate = null;
                    this.postProcessTicket(data);
                },
                (response) => {
                    this.error = response.responseJSON["detail"];
                });
        },
    }
}
Vue.createApp(TicketsApp).mount('#ticketsApp')