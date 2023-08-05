## -*- coding: utf-8; -*-
<%inherit file="/master/create.mako" />

<%def name="extra_styles()">
  ${parent.extra_styles()}
  % if use_buefy:
      <style type="text/css">
        .this-page-content {
            flex-grow: 1;
        }
      </style>
  % endif
</%def>

<%def name="page_content()">
  <br />
  % if use_buefy:
      <customer-order-creator></customer-order-creator>
  % else:
      <p>Sorry, but this page is not supported by your current theme configuration.</p>
  % endif
</%def>

<%def name="order_form_buttons()">
  <div class="level">
    <div class="level-left">
    </div>
    <div class="level-right">
      <div class="level-item">
        <div class="buttons">
          <b-button type="is-primary"
                    @click="submitOrder()"
                    :disabled="submittingOrder"
                    icon-pack="fas"
                    icon-left="fas fa-upload">
            {{ submitOrderButtonText }}
          </b-button>
          <b-button @click="startOverEntirely()"
                    icon-pack="fas"
                    icon-left="fas fa-redo">
            Start Over Entirely
          </b-button>
          <b-button @click="cancelOrder()"
                    type="is-danger"
                    icon-pack="fas"
                    icon-left="fas fa-trash">
            Cancel this Order
          </b-button>
        </div>
      </div>
    </div>
  </div>
</%def>

<%def name="render_this_page_template()">
  ${parent.render_this_page_template()}

  <script type="text/x-template" id="customer-order-creator-template">
    <div>

      ${self.order_form_buttons()}

      <b-collapse class="panel" :class="customerPanelType"
                  :open.sync="customerPanelOpen">

        <div slot="trigger"
             slot-scope="props"
             class="panel-heading"
             role="button">
          <b-icon pack="fas"
            ## TODO: this icon toggling should work, according to
            ## Buefy docs, but i could not ever get it to work.
            ## what am i missing?
            ## https://buefy.org/documentation/collapse/
            ## :icon="props.open ? 'caret-down' : 'caret-right'">
            ## (for now we just always show caret-right instead)
            icon="caret-right">
          </b-icon>
          <strong v-html="customerPanelHeader"></strong>
        </div>

        <div class="panel-block">
          <div style="width: 100%;">

            <div style="display: flex; flex-direction: row;">
              <div style="flex-grow: 1; margin-right: 1rem;">
                <b-notification :type="customerStatusType"
                                position="is-bottom-right"
                                :closable="false">
                  {{ customerStatusText }}
                </b-notification>
              </div>
              <!-- <div class="buttons"> -->
              <!--   <b-button @click="startOverCustomer()" -->
              <!--             icon-pack="fas" -->
              <!--             icon-left="fas fa-redo"> -->
              <!--     Start Over -->
              <!--   </b-button> -->
              <!-- </div> -->
            </div>

            <br />
            <div class="field">
              <b-radio v-model="contactIsKnown"
                       :native-value="true">
                Customer is already in the system.
              </b-radio>
            </div>

            <div v-show="contactIsKnown"
                 style="padding-left: 10rem;">

              <b-field label="Customer" grouped>
                <b-field style="margin-left: 1rem;""
                         :expanded="!contactUUID">
                  <tailbone-autocomplete ref="contactAutocomplete"
                                         v-model="contactUUID"
                                         placeholder="Enter name or phone number"
                                         :initial-label="contactDisplay"
                                         % if new_order_requires_customer:
                                         serviceUrl="${url('{}.customer_autocomplete'.format(route_prefix))}"
                                         % else:
                                         serviceUrl="${url('{}.person_autocomplete'.format(route_prefix))}"
                                         % endif
                                         @input="contactChanged">
                  </tailbone-autocomplete>
                </b-field>
                <b-button v-if="contactUUID && contactProfileURL"
                          type="is-primary"
                          tag="a" target="_blank"
                          :href="contactProfileURL"
                          icon-pack="fas"
                          icon-left="external-link-alt">
                  View Profile
                </b-button>
              </b-field>

              <b-field grouped v-show="contactUUID"
                       style="margin-top: 2rem;">

                <b-field label="Phone Number"
                         style="margin-right: 3rem;">
                  <div class="level">
                    <div class="level-left">
                      <div class="level-item">
                        {{ orderPhoneNumber }}
                      </div>
                      <div class="level-item">
                        <b-button type="is-primary"
                                  @click="editPhoneNumberInit()"
                                  icon-pack="fas"
                                  icon-left="edit">
                          Edit
                        </b-button>

                        <b-modal has-modal-card
                                 :active.sync="editPhoneNumberShowDialog">
                          <div class="modal-card">

                            <header class="modal-card-head">
                              <p class="modal-card-title">Edit Phone Number</p>
                            </header>

                            <section class="modal-card-body">
                              <b-field label="Phone Number"
                                       :type="editPhoneNumberValue ? null : 'is-danger'">
                                <b-input v-model="editPhoneNumberValue"
                                         ref="editPhoneNumberInput">
                                </b-input>
                              </b-field>
                            </section>

                            <footer class="modal-card-foot">
                              <b-button type="is-primary"
                                        icon-pack="fas"
                                        icon-left="save"
                                        :disabled="editPhoneNumberSaveDisabled"
                                        @click="editPhoneNumberSave()">
                                {{ editPhoneNumberSaveText }}
                              </b-button>
                              <b-button @click="editPhoneNumberShowDialog = false">
                                Cancel
                              </b-button>
                            </footer>
                          </div>
                        </b-modal>

                      </div>
                    </div>
                  </div>
                </b-field>

                <b-field label="Email Address">
                  <div class="level">
                    <div class="level-left">
                      <div class="level-item">
                        <span v-if="orderEmailAddress">
                          {{ orderEmailAddress }}
                        </span>
                        <span v-if="!orderEmailAddress"
                              class="has-text-danger">
                          (no valid email on file)
                        </span>
                      </div>
                      <div class="level-item">
                        <b-button type="is-primary"
                                  @click="editEmailAddressInit()"
                                  icon-pack="fas"
                                  icon-left="edit">
                          Edit
                        </b-button>
                        <b-modal has-modal-card
                                 :active.sync="editEmailAddressShowDialog">
                          <div class="modal-card">

                            <header class="modal-card-head">
                              <p class="modal-card-title">Edit Email Address</p>
                            </header>

                            <section class="modal-card-body">
                              <b-field label="Email Address"
                                       :type="editEmailAddressValue ? null : 'is-danger'">
                                <b-input v-model="editEmailAddressValue"
                                         ref="editEmailAddressInput">
                                </b-input>
                              </b-field>
                            </section>

                            <footer class="modal-card-foot">
                              <b-button type="is-primary"
                                        icon-pack="fas"
                                        icon-left="save"
                                        :disabled="editEmailAddressSaveDisabled"
                                        @click="editEmailAddressSave()">
                                {{ editEmailAddressSaveText }}
                              </b-button>
                              <b-button @click="editEmailAddressShowDialog = false">
                                Cancel
                              </b-button>
                            </footer>
                          </div>
                        </b-modal>
                      </div>
                    </div>
                  </div>
                </b-field>

              </b-field>
            </div>

            <br />
            <div class="field">
              <b-radio v-model="contactIsKnown" disabled
                       :native-value="false">
                Customer is not yet in the system.
              </b-radio>
            </div>

            <div v-if="!contactIsKnown">
              <b-field label="Customer Name" horizontal>
                <b-input v-model="customerName"></b-input>
              </b-field>
              <b-field label="Phone Number" horizontal>
                <b-input v-model="phoneNumber"></b-input>
              </b-field>
            </div>

          </div>
        </div> <!-- panel-block -->
      </b-collapse>

      <b-collapse class="panel"
                  open>

        <div slot="trigger"
             slot-scope="props"
             class="panel-heading"
             role="button">
          <b-icon pack="fas"
            ## TODO: this icon toggling should work, according to
            ## Buefy docs, but i could not ever get it to work.
            ## what am i missing?
            ## https://buefy.org/documentation/collapse/
            ## :icon="props.open ? 'caret-down' : 'caret-right'">
            ## (for now we just always show caret-right instead)
            icon="caret-right">
          </b-icon>
          <strong v-html="itemsPanelHeader"></strong>
        </div>

        <div class="panel-block">
          <div>
            <div class="buttons">
              <b-button type="is-primary"
                        icon-pack="fas"
                        icon-left="fas fa-plus"
                        @click="showAddItemDialog()">
                Add Item
              </b-button>
            </div>
            <b-modal :active.sync="showingItemDialog">
              <div class="card">
                <div class="card-content">

                  <b-tabs type="is-boxed is-toggle"
                          :animated="false">

                    <b-tab-item label="Product">

                      <div class="field">
                        <b-radio v-model="productIsKnown"
                                 :native-value="true">
                          Product is already in the system.
                        </b-radio>
                      </div>

                      <div v-show="productIsKnown">

                        <b-field grouped>
                          <b-field label="Description" horizontal expanded>
                            <tailbone-autocomplete
                               ref="productDescriptionAutocomplete"
                               v-model="productUUID"
                               :assigned-value="productUUID"
                               :assigned-label="productDisplay"
                               serviceUrl="${product_autocomplete_url}"
                               @input="productChanged">
                            </tailbone-autocomplete>
                          </b-field>
                        </b-field>

                        <b-field grouped>
                          <b-field label="UPC" horizontal expanded>
                            <b-input v-if="!productUUID"
                                     v-model="productUPC"
                                     ref="productUPCInput"
                                     @keydown.native="productUPCKeyDown">
                            </b-input>
                            <b-button v-if="!productUUID"
                                      type="is-primary"
                                      icon-pack="fas"
                                      icon-left="search"
                                      @click="fetchProductByUPC()">
                              Fetch
                            </b-button>
                            <b-button v-if="productUUID"
                                      @click="clearProduct(true)">
                              {{ productUPC }} (click to change)
                            </b-button>
                          </b-field>
                          <b-button v-if="productUUID"
                                    type="is-primary"
                                    tag="a" target="_blank"
                                    :href="'${request.route_url('products')}/' + productUUID"
                                    icon-pack="fas"
                                    icon-left="external-link-alt">
                            View Product
                          </b-button>
                        </b-field>

                      </div>

                      <div class="field">
                        <b-radio v-model="productIsKnown" disabled
                                 :native-value="false">
                          Product is not yet in the system.
                        </b-radio>
                      </div>

                    </b-tab-item>
                    <b-tab-item label="Quantity">

                      <b-field grouped>

                        <b-field label="Quantity" horizontal>
                          <b-input v-model="productQuantity"></b-input>
                        </b-field>

                        <b-select v-model="productUOM">
                          <option v-for="choice in productUnitChoices"
                                  :key="choice.key"
                                  :value="choice.key"
                                  v-html="choice.value">
                          </option>
                        </b-select>

                      </b-field>
                    </b-tab-item>
                  </b-tabs>

                  <div class="buttons">
                    <b-button @click="showingItemDialog = false">
                      Cancel
                    </b-button>
                    <b-button type="is-primary"
                              icon-pack="fas"
                              icon-left="fas fa-save"
                              @click="itemDialogSave()">
                      {{ itemDialogSaveButtonText }}
                    </b-button>
                  </div>

                </div>
              </div>
            </b-modal>

            <b-table v-if="items.length"
                     :data="items">
              <template slot-scope="props">

                <b-table-column field="product_upc_pretty" label="UPC">
                  {{ props.row.product_upc_pretty }}
                </b-table-column>

                <b-table-column field="product_brand" label="Brand">
                  {{ props.row.product_brand }}
                </b-table-column>

                <b-table-column field="product_description" label="Description">
                  {{ props.row.product_description }}
                </b-table-column>

                <b-table-column field="product_size" label="Size">
                  {{ props.row.product_size }}
                </b-table-column>

                <b-table-column field="department_display" label="Department">
                  {{ props.row.department_display }}
                </b-table-column>

                <b-table-column field="order_quantity_display" label="Quantity">
                  <span v-html="props.row.order_quantity_display"></span>
                </b-table-column>

                <b-table-column field="total_price_display" label="Total">
                  {{ props.row.total_price_display }}
                </b-table-column>

                <b-table-column field="vendor_display" label="Vendor">
                  {{ props.row.vendor_display }}
                </b-table-column>

                <b-table-column field="actions" label="Actions">
                  <a href="#" class="grid-action"
                     @click.prevent="showEditItemDialog(props.index)">
                    <i class="fas fa-edit"></i>
                    Edit
                  </a>
                  &nbsp;

                  <a href="#" class="grid-action has-text-danger"
                     @click.prevent="deleteItem(props.index)">
                    <i class="fas fa-trash"></i>
                    Delete
                  </a>
                  &nbsp;
                </b-table-column>

              </template>
            </b-table>
          </div>
        </div>
      </b-collapse>

      ${self.order_form_buttons()}

      ${h.form(request.current_route_url(), ref='batchActionForm')}
      ${h.csrf_token(request)}
      ${h.hidden('action', **{'v-model': 'batchAction'})}
      ${h.end_form()}

    </div>
  </script>
</%def>

<%def name="make_this_page_component()">
  ${parent.make_this_page_component()}
  <script type="text/javascript">

    const CustomerOrderCreator = {
        template: '#customer-order-creator-template',
        data() {

            ## TODO: these should come from handler
            let defaultUnitChoices = [
                {key: '${enum.UNIT_OF_MEASURE_EACH}', value: "Each"},
                {key: '${enum.UNIT_OF_MEASURE_POUND}', value: "Pound"},
                {key: '${enum.UNIT_OF_MEASURE_CASE}', value: "Case"},
            ]
            let defaultUOM = '${enum.UNIT_OF_MEASURE_CASE}'

            return {
                batchAction: null,
                batchTotalPriceDisplay: ${json.dumps(normalized_batch['total_price_display'])|n},

                customerPanelOpen: false,
                contactIsKnown: true,
                contactUUID: ${json.dumps(batch.customer_uuid)|n},
                contactDisplay: ${json.dumps(six.text_type(batch.customer or ''))|n},
                customerEntry: null,
                contactProfileURL: ${json.dumps(contact_profile_url)|n},
                ## phoneNumberEntry: ${json.dumps(batch.phone_number)|n},
                orderPhoneNumber: ${json.dumps(batch.phone_number)|n},
                phoneNumberSaved: true,
                customerName: null,
                phoneNumber: null,
                orderEmailAddress: ${json.dumps(batch.email_address)|n},

                editPhoneNumberShowDialog: false,
                editPhoneNumberValue: null,
                editPhoneNumberSaving: false,

                editEmailAddressShowDialog: false,
                editEmailAddressValue: null,
                editEmailAddressSaving: false,

                items: ${json.dumps(order_items)|n},
                editingItem: null,
                showingItemDialog: false,
                productIsKnown: true,
                productUUID: null,
                productDisplay: null,
                productUPC: null,
                productQuantity: null,
                defaultUnitChoices: defaultUnitChoices,
                productUnitChoices: defaultUnitChoices,
                defaultUOM: defaultUOM,
                productUOM: defaultUOM,
                productCaseSize: null,

                ## TODO: should find a better way to handle CSRF token
                csrftoken: ${json.dumps(request.session.get_csrf_token() or request.session.new_csrf_token())|n},

                submittingOrder: false,
            }
        },
        computed: {
            customerPanelHeader() {
                let text = "Customer"

                if (this.contactIsKnown) {
                    if (this.contactUUID) {
                        if (this.$refs.contactAutocomplete) {
                            text = "Customer: " + this.$refs.contactAutocomplete.getDisplayText()
                        } else {
                            text = "Customer: " + this.contactDisplay
                        }
                    }
                } else {
                    if (this.customerName) {
                        text = "Customer: " + this.customerName
                    }
                }

                if (!this.customerPanelOpen) {
                    text += ' <p class="' + this.customerHeaderClass + '" style="display: inline-block; float: right;">' + this.customerStatusText + '</p>'
                }

                return text
            },
            customerHeaderClass() {
                if (!this.customerPanelOpen) {
                    if (this.customerStatusType == 'is-danger') {
                        return 'has-text-danger'
                    } else if (this.customerStatusType == 'is-warning') {
                        return 'has-text-warning'
                    }
                }
            },
            customerPanelType() {
                if (!this.customerPanelOpen) {
                    return this.customerStatusType
                }
            },
            customerStatusType() {
                return this.customerStatusTypeAndText.type
            },
            customerStatusText() {
                return this.customerStatusTypeAndText.text
            },
            customerStatusTypeAndText() {
                let phoneNumber = null
                if (this.contactIsKnown) {
                    if (!this.contactUUID) {
                        return {
                            type: 'is-danger',
                            text: "Please identify the customer.",
                        }
                    }
                    if (!this.orderPhoneNumber) {
                        return {
                            type: 'is-warning',
                            text: "Please provide a phone number for the customer.",
                        }
                    }
                    phoneNumber = this.orderPhoneNumber
                } else { // customer is not known
                    if (!this.customerName) {
                        return {
                            type: 'is-danger',
                            text: "Please identify the customer.",
                        }
                    }
                    if (!this.phoneNumber) {
                        return {
                            type: 'is-warning',
                            text: "Please provide a phone number for the customer.",
                        }
                    }
                    phoneNumber = this.phoneNumber
                }

                let phoneDigits = phoneNumber.replace(/\D/g, '')
                if (!phoneDigits.length || (phoneDigits.length != 7 && phoneDigits.length != 10)) {
                    return {
                        type: 'is-warning',
                        text: "The phone number does not appear to be valid.",
                    }
                }

                if (!this.contactIsKnown) {
                    return {
                        type: 'is-warning',
                        text: "Will create a new customer record.",
                    }
                }

                return {
                    type: null,
                    text: "Customer info looks okay.",
                }
            },

            editPhoneNumberSaveDisabled() {
                if (this.editPhoneNumberSaving) {
                    return true
                }
                if (!this.editPhoneNumberValue) {
                    return true
                }
                return false
            },

            editPhoneNumberSaveText() {
                if (this.editPhoneNumberSaving) {
                    return "Working, please wait..."
                }
                return "Save"
            },

            editEmailAddressSaveDisabled() {
                if (this.editEmailAddressSaving) {
                    return true
                }
                if (!this.editEmailAddressValue) {
                    return true
                }
                return false
            },

            editEmailAddressSaveText() {
                if (this.editEmailAddressSaving) {
                    return "Working, please wait..."
                }
                return "Save"
            },

            itemsPanelHeader() {
                let text = "Items"

                if (this.items.length) {
                    text = "Items: " + this.items.length.toString() + " for " + this.batchTotalPriceDisplay
                }

                return text
            },

            itemDialogSaveButtonText() {
                return this.editingItem ? "Update Item" : "Add Item"
            },

            submitOrderButtonText() {
                if (this.submittingOrder) {
                    return "Working, please wait..."
                }
                return "Submit this Order"
            },
        },
        mounted() {
            if (this.customerStatusType) {
                this.customerPanelOpen = true
            }
        },
        methods: {

            startOverEntirely() {
                let msg = "Are you sure you want to start over entirely?\n\n"
                    + "This will totally delete this order and start a new one."
                if (!confirm(msg)) {
                    return
                }
                this.batchAction = 'start_over_entirely'
                this.$nextTick(function() {
                    this.$refs.batchActionForm.submit()
                })
            },

            // startOverCustomer(confirmed) {
            //     if (!confirmed) {
            //         let msg = "Are you sure you want to start over for the customer data?"
            //         if (!confirm(msg)) {
            //             return
            //         }
            //     }
            //     this.contactIsKnown = true
            //     this.contactUUID = null
            //     // this.customerEntry = null
            //     this.phoneNumberEntry = null
            //     this.customerName = null
            //     this.phoneNumber = null
            // },

            // startOverItem(confirmed) {
            //     if (!confirmed) {
            //         let msg = "Are you sure you want to start over for the item data?"
            //         if (!confirm(msg)) {
            //             return
            //         }
            //     }
            //     // TODO: reset things
            // },

            cancelOrder() {
                let msg = "Are you sure you want to cancel?\n\n"
                    + "This will totally delete the current order."
                if (!confirm(msg)) {
                    return
                }
                this.batchAction = 'delete_batch'
                this.$nextTick(function() {
                    this.$refs.batchActionForm.submit()
                })
            },

            submitBatchData(params, callback) {
                let url = ${json.dumps(request.current_route_url())|n}
                
                let headers = {
                    ## TODO: should find a better way to handle CSRF token
                    'X-CSRF-TOKEN': this.csrftoken,
                }

                ## TODO: should find a better way to handle CSRF token
                this.$http.post(url, params, {headers: headers}).then((response) => {
                    if (callback) {
                        callback(response)
                    }
                }, response => {
                    this.$buefy.toast.open({
                        message: "Unexpected error occurred",
                        type: 'is-danger',
                        duration: 2000, // 2 seconds
                    })
                })
            },

            submitOrder() {
                this.submittingOrder = true

                let params = {
                    action: 'submit_new_order',
                }

                this.submitBatchData(params, response => {
                    if (response.data.error) {
                        this.$buefy.toast.open({
                            message: "Submit failed: " + response.data.error,
                            type: 'is-danger',
                            duration: 2000, // 2 seconds
                        })
                        this.submittingOrder = false
                    } else {
                        if (response.data.next_url) {
                            location.href = response.data.next_url
                        } else {
                            location.reload()
                        }
                    }
                })
            },

            contactChanged(uuid) {
                let params
                if (!uuid) {
                    params = {
                        action: 'unassign_contact',
                    }
                } else {
                    params = {
                        action: 'assign_contact',
                        uuid: this.contactUUID,
                    }
                }
                let that = this
                this.submitBatchData(params, function(response) {
                    console.log(response.data)
                    % if new_order_requires_customer:
                    that.contactUUID = response.data.customer_uuid
                    % else:
                    that.contactUUID = response.data.person_uuid
                    % endif
                    that.orderPhoneNumber = response.data.phone_number
                    that.orderEmailAddress = response.data.email_address
                    that.contactProfileURL = response.data.contact_profile_url
                })
            },

            editPhoneNumberInit() {
                this.editPhoneNumberValue = this.orderPhoneNumber
                this.editPhoneNumberShowDialog = true
                this.$nextTick(() => {
                    this.$refs.editPhoneNumberInput.focus()
                })
            },

            editPhoneNumberSave() {
                this.editPhoneNumberSaving = true

                let params = {
                    action: 'update_phone_number',
                    phone_number: this.editPhoneNumberValue,
                }

                this.submitBatchData(params, response => {
                    if (response.data.success) {
                        this.orderPhoneNumber = response.data.phone_number
                        this.editPhoneNumberShowDialog = false
                    } else {
                        this.$buefy.toast.open({
                            message: "Save failed: " + response.data.error,
                            type: 'is-danger',
                            duration: 2000, // 2 seconds
                        })
                    }
                    this.editPhoneNumberSaving = false
                })

            },

            editEmailAddressInit() {
                this.editEmailAddressValue = this.orderEmailAddress
                this.editEmailAddressShowDialog = true
                this.$nextTick(() => {
                    this.$refs.editEmailAddressInput.focus()
                })
            },

            editEmailAddressSave() {
                this.editEmailAddressSaving = true

                let params = {
                    action: 'update_email_address',
                    email_address: this.editEmailAddressValue,
                }

                this.submitBatchData(params, response => {
                    if (response.data.success) {
                        this.orderEmailAddress = response.data.email_address
                        this.editEmailAddressShowDialog = false
                    } else {
                        this.$buefy.toast.open({
                            message: "Save failed: " + response.data.error,
                            type: 'is-danger',
                            duration: 2000, // 2 seconds
                        })
                    }
                    this.editEmailAddressSaving = false
                })

            },

            showAddItemDialog() {
                this.customerPanelOpen = false
                this.editingItem = null
                this.productIsKnown = true
                this.productUUID = null
                this.productDisplay = null
                this.productUPC = null
                this.productQuantity = 1
                this.productUnitChoices = this.defaultUnitChoices
                this.productUOM = this.defaultUOM
                this.showingItemDialog = true
                this.$nextTick(() => {
                    this.$refs.productDescriptionAutocomplete.focus()
                })
            },

            showEditItemDialog(index) {
                row = this.items[index]
                this.editingItem = row
                this.productIsKnown = true // TODO
                this.productUUID = row.product_uuid
                this.productDisplay = row.product_full_description
                this.productUPC = row.product_upc_pretty || row.product_upc
                this.productQuantity = row.order_quantity
                this.productUnitChoices = row.order_uom_choices
                this.productUOM = row.order_uom

                this.showingItemDialog = true
            },

            deleteItem(index) {
                if (!confirm("Are you sure you want to delete this item?")) {
                    return
                }

                let params = {
                    action: 'delete_item',
                    uuid: this.items[index].uuid,
                }
                this.submitBatchData(params, response => {
                    if (response.data.error) {
                        this.$buefy.toast.open({
                            message: "Delete failed:  " + response.data.error,
                            type: 'is-warning',
                            duration: 2000, // 2 seconds
                        })
                    } else {
                        this.items.splice(index, 1)
                        this.batchTotalPriceDisplay = response.data.batch.total_price_display
                    }
                })
            },

            clearProduct(autofocus) {
                this.productUUID = null
                this.productDisplay = null
                this.productUPC = null
                this.productUnitChoices = this.defaultUnitChoices
                if (autofocus) {
                    this.$nextTick(() => {
                        this.$refs.productUPCInput.focus()
                    })
                }
            },

            setProductUnitChoices(choices) {
                this.productUnitChoices = choices

                let found = false
                for (let uom of choices) {
                    if (this.productUOM == uom.key) {
                        found = true
                        break
                    }
                }
                if (!found) {
                    this.productUOM = choices[0].key
                }
            },

            fetchProductByUPC() {
                let params = {
                    action: 'find_product_by_upc',
                    upc: this.productUPC,
                }
                this.submitBatchData(params, response => {
                    if (response.data.error) {
                        this.$buefy.toast.open({
                            message: "Fetch failed:  " + response.data.error,
                            type: 'is-warning',
                            duration: 2000, // 2 seconds
                        })
                    } else {
                        this.productUUID = response.data.uuid
                        this.productUPC = response.data.upc_pretty
                        this.productDisplay = response.data.full_description
                        this.setProductUnitChoices(response.data.uom_choices)
                    }
                })
            },

            productUPCKeyDown(event) {
                if (event.which == 13) { // Enter
                    this.fetchProductByUPC()
                }
            },

            productChanged(uuid) {
                if (uuid) {
                    this.productUUID = uuid
                    let params = {
                        action: 'get_product_info',
                        uuid: this.productUUID,
                    }
                    this.submitBatchData(params, response => {
                        this.productUPC = response.data.upc_pretty
                        this.productDisplay = response.data.full_description
                        this.setProductUnitChoices(response.data.uom_choices)
                    })
                } else {
                    this.clearProduct()
                }
            },

            itemDialogSave() {

                let params = {
                    product_is_known: this.productIsKnown,
                    product_uuid: this.productUUID,
                    order_quantity: this.productQuantity,
                    order_uom: this.productUOM,
                }

                if (this.editingItem) {
                    params.action = 'update_item'
                    params.uuid = this.editingItem.uuid
                } else {
                    params.action = 'add_item'
                }

                this.submitBatchData(params, response => {

                    if (params.action == 'add_item') {
                        this.items.push(response.data.row)

                    } else { // update_item
                        // must update each value separately, instead of
                        // overwriting the item record, or else display will
                        // not update properly
                        for (let [key, value] of Object.entries(response.data.row)) {
                            this.editingItem[key] = value
                        }
                    }

                    // also update the batch total price
                    this.batchTotalPriceDisplay = response.data.batch.total_price_display

                    this.showingItemDialog = false
                })
            },
        },
    }

    Vue.component('customer-order-creator', CustomerOrderCreator)

  </script>
</%def>


${parent.body()}
