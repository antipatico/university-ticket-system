const TicketListItem = {
    props: {
        ticket: Object,
        showOwner: Boolean,
    },
    template: `
<li class="list-group-item">
  <div class="row" v-if="showOwner">
    <div class="col-xl-4 col-lg-12">
      <span v-if="ticket.is_closed" class="click bi text-muted" :class="QACommon.getIconClass(ticket.status)"  v-on:click="openTicketDetails(ticket.id)">&nbsp;<del>{{ticket.name}}</del></span>
      <span v-else class="click bi" :class="QACommon.getIconClass(ticket.status)"  v-on:click="openTicketDetails(ticket.id)">&nbsp;<strong>{{ticket.name}}</strong></span>
    </div>
    <div class="col-xl-4 col-lg-7 col-md-12">
      <span>{{ticket.owner.name}}</span>
    </div>
    <div class="col-xl-4 col-lg-5 col-md-12">
       <small v-if="ticket.is_closed" class="text-muted">Chiuso il {{QACommon.dateToStringNumeric(ticket.ts_closed)}}</small>
       <small v-else>Creato il {{QACommon.dateToStringNumeric(ticket.ts_open)}}</small>
    </div>
  </div>
  <div class="row" v-else>
    <div class="col-xl-8 col-lg-12">
      <span v-if="ticket.is_closed" class="click bi text-muted" :class="QACommon.getIconClass(ticket.status)"  v-on:click="openTicketDetails(ticket.id)">&nbsp;<del>{{ticket.name}}</del></span>
      <span v-else class="click bi" :class="QACommon.getIconClass(ticket.status)"  v-on:click="openTicketDetails(ticket.id)">&nbsp;<strong>{{ticket.name}}</strong></span>
    </div>
    <div class="col-xl-4 col-lg-12">
       <small v-if="ticket.is_closed" class="text-muted">Chiuso il {{QACommon.dateToStringNumeric(ticket.ts_closed)}}</small>
       <small v-else>Creato il {{QACommon.dateToStringNumeric(ticket.ts_open)}}</small>
    </div>
  </div>
</li>`,
}