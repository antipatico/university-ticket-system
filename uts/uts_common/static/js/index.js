
const TicketsApp = {
    delimiters: ['$%','%$'],
    data() {
        return {
            openedTicket: null,
            recentTickets: [
                {
                    "id": 6,
                    "owner": {
                        "id": 3,
                        "name": "org1",
                        "type": "organization"
                    },
                    "status": "CLOSED",
                    "name": "orgticket",
                    "description": "test",
                    "events": [
                        {
                            "id": 4,
                            "owner": {
                                "id": 3,
                                "name": "org1",
                                "type": "organization"
                            },
                            "status": "NOTE",
                            "timestamp": "2021-05-02T13:14:32.821286Z",
                            "info": ""
                        },
                        {
                            "id": 3,
                            "owner": {
                                "id": 1,
                                "name": "admin admin",
                                "type": "individual"
                            },
                            "status": "INFO_NEEDED",
                            "timestamp": "2021-05-02T13:10:29.673343Z",
                            "info": ""
                        },
                        {
                            "id": 2,
                            "owner": {
                                "id": 2,
                                "name": "user user",
                                "type": "individual"
                            },
                            "status": "INFO_NEEDED",
                            "timestamp": "2021-05-02T13:10:21.319360Z",
                            "info": ""
                        }
                    ],
                    "tags": [
                        "afdas",
                        "lmao!"
                    ],
                    "ts_open": "2021-05-02T11:27:12.856469Z",
                    "ts_last_modified": "2021-05-02T12:50:14.058296Z",
                    "ts_closed": null,
                    "is_closed": true
                },
                {
                    "id": 2,
                    "owner": {
                        "id": 1,
                        "name": "admin admin",
                        "type": "individual"
                    },
                    "status": "OPEN",
                    "name": "ticket1",
                    "description": "desc1",
                    "events": [],
                    "tags": [
                        "afdas"
                    ],
                    "ts_open": "2021-05-02T10:53:01.013125Z",
                    "ts_last_modified": "2021-05-02T12:40:29.856349Z",
                    "ts_closed": null,
                    "is_closed": false
                },
                {
                    "id": 3,
                    "owner": {
                        "id": 1,
                        "name": "admin admin",
                        "type": "individual"
                    },
                    "status": "DUPLICATE",
                    "name": "ticket2",
                    "description": "desc2",
                    "events": [],
                    "tags": [],
                    "ts_open": "2021-05-02T10:53:11.376866Z",
                    "ts_last_modified": "2021-05-02T11:16:30.576092Z",
                    "ts_closed": null,
                    "is_closed": false
                }
            ]
        }
    },
    mounted() {
        console.log("App mounted")
    },
    methods: {
        getIconClass(status) {
            switch (status) {
                case "OPEN":
                    return "bi-envelope-open"
                case "CLOSED":
                    return "bi-envelope"
                case "DUPLICATE":
                    return "bi-intersect"
                case "ESCALATION":
                    return "bi-file-earmark-person"
                case "NOTE":
                    return "bi-vector-pen"
                case "INFO_NEEDED":
                    return "bi-info-circle"
                case "ANSWER":
                    return "bi-award"
            }
        },
        getEventMessage(status) {
            switch (status) {
                case "OPEN":
                    return "ha aperto il ticket"
                case "CLOSED":
                    return "ha chiuso il ticket"
                case "DUPLICATE":
                    return "ha marcato il ticket come duplicato"
                case "ESCALATION":
                    return "ha passato la proprietà del ticket"
                case "NOTE":
                    return "ha aggiunto una nota"
                case "INFO_NEEDED":
                    return "ha richiesto informazioni aggiuntive"
                case "ANSWER":
                    return "ha risposto"
            }
        }
    }
}
Vue.createApp(TicketsApp).mount('#ticketsApp')