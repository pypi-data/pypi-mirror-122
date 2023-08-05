# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2021 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Handler for "customer order" batches
"""

from __future__ import unicode_literals, absolute_import, division

import re

import six
import sqlalchemy as sa
from sqlalchemy import orm

from rattail.db import model
from rattail.batch import BatchHandler


class CustomerOrderBatchHandler(BatchHandler):
    """
    Handler for all "customer order" batches, regardless of "mode".  The
    handler must inspect the
    :attr:`~rattail.db.model.batch.custorder.CustomerOrderBatch.mode` attribute
    of each batch it deals with, in order to determine which logic to apply.

    .. attribute:: has_custom_product_autocomplete

       If true, this flag indicates that the handler provides custom
       autocomplete logic for use when selecting a product while
       creating a new order.
    """
    batch_model_class = model.CustomerOrderBatch
    has_custom_product_autocomplete = False
    nondigits_pattern = re.compile(r'\D')

    def init_batch(self, batch, progress=None, **kwargs):
        """
        Assign the "local" store to the batch, if applicable.
        """
        session = self.app.get_session(batch)
        batch.store = self.config.get_store(session)

    def new_order_requires_customer(self):
        """
        Returns a boolean indicating whether a *new* "customer order"
        in fact requires a proper customer account, or not.  Note that
        in all cases a new order requires a *person* to associate
        with, but technically the customer is optional, unless this
        returns true.
        """
        return self.config.getbool('rattail.custorders',
                                   'new_order_requires_customer',
                                   default=False)

    def assign_contact(self, batch, customer=None, person=None, **kwargs):
        """
        Assign the customer and/or person "contact" for the order.
        """
        clientele = self.app.get_clientele_handler()
        customer_required = self.new_order_requires_customer()

        # nb. person is always required
        if customer and not person:
            person = clientele.get_person(customer)
        if not person:
            raise ValueError("Must specify a person")

        # customer may or may not be optional
        if person and not customer:
            customer = clientele.get_customer(person)
        if customer_required and not customer:
            raise ValueError("Must specify a customer account")

        # assign contact
        batch.customer = customer
        batch.person = person

        # update phone/email per new contact
        batch.phone_number = None
        batch.email_address = None
        if customer_required:
            batch.phone_number = clientele.get_first_phone_number(customer)
            batch.email_address = clientele.get_first_email_address(customer)
        else:
            batch.phone_number = person.first_phone_number()
            batch.email_address = person.first_email_address()

        session = self.app.get_session(batch)
        session.flush()
        session.refresh(batch)

    def unassign_contact(self, batch, **kwargs):
        """
        Unassign the customer and/or person "contact" for the order.
        """
        batch.customer = None
        batch.person = None
        batch.phone_number = None
        batch.email_address = None

        session = self.app.get_session(batch)
        session.flush()
        session.refresh(batch)

    def get_case_size_for_product(self, product):
        if product.case_size:
            return product.case_size

        cost = product.cost
        if cost:
            return cost.case_size

    def get_phone_search_term(self, term):
        """
        Try to figure out if the given search term represents a whole
        or partial phone number, and if so return just the digits.
        """
        digits = self.nondigits_pattern.sub('', term)
        if digits and len(digits) >= 4:
            return digits

    def customer_autocomplete(self, session, term, **kwargs):
        """
        Override the Customer autocomplete, to search by phone number
        as well as name.
        """
        model = self.model

        # define the base query
        query = session.query(model.Customer)\
                       .options(orm.joinedload(model.Customer.phones))

        # does search term look like a phone number?
        phone_term = self.get_phone_search_term(term)
        if phone_term:

            # yep, so just search for the phone number
            query = query.join(model.CustomerPhoneNumber,
                               model.CustomerPhoneNumber.parent_uuid == model.Customer.uuid)
            query = query.filter(sa.func.regexp_replace(model.CustomerPhoneNumber.number,
                                                        r'\D', '', 'g')\
                                 .like('%{}%'.format(phone_term)))

        else: # term does not look like a phone number

            # so just search by name
            criteria = [model.Customer.name.ilike('%{}%'.format(word))
                        for word in term.split()]
            query = query.filter(sa.and_(*criteria))

        # oh, and sort by something useful
        query = query.order_by(model.Customer.name)

        # generate result list from query
        results = []
        for customer in query:
            phone = customer.first_phone()
            if phone:
                label = "{} {}".format(customer.name, phone.number)
            else:
                label = customer.name
            results.append({'value': customer.uuid,
                            'label': label,
                            'display': customer.name})

        return results

    def person_autocomplete(self, session, term, **kwargs):
        """
        Override the Person autocomplete, to search by phone number as
        well as name.
        """
        model = self.model

        # define the base query
        query = session.query(model.Person)\
                       .options(orm.joinedload(model.Person.phones))

        # does search term look like a phone number?
        phone_term = self.get_phone_search_term(term)
        if phone_term:

            # yep, so just search for the phone number
            query = query.join(model.PersonPhoneNumber,
                               model.PersonPhoneNumber.parent_uuid == model.Person.uuid)
            query = query.filter(sa.func.regexp_replace(model.PersonPhoneNumber.number,
                                                        r'\D', '', 'g')\
                                 .like('%{}%'.format(phone_term)))

        else: # term does not look like a phone number

            # so just search by name
            criteria = [model.Person.display_name.ilike('%{}%'.format(word))
                        for word in term.split()]
            query = query.filter(sa.and_(*criteria))

        # oh, and sort by something useful
        query = query.order_by(model.Person.display_name)

        # generate result list from query
        results = []
        for person in query:
            phone = person.first_phone()
            if phone:
                label = "{} {}".format(person.display_name, phone.number)
            else:
                label = person.display_name
            results.append({'value': person.uuid,
                            'label': label,
                            'display': person.display_name})

        return results

    def get_customer_info(self, batch, **kwargs):
        """
        Return a data dict containing misc. info pertaining to the
        customer/person for the order batch.
        """
        info = {
            'customer_uuid': None,
            'person_uuid': None,
            'phone_number': None,
            'email_address': None,
        }

        if batch.customer:
            info['customer_uuid'] = batch.customer.uuid
            phone = batch.customer.first_phone()
            if phone:
                info['phone_number'] = phone.number
            email = batch.customer.first_email()
            if email:
                info['email_address'] = email.address

        if batch.person:
            info['person_uuid'] = batch.person.uuid
            if not info['phone_number']:
                phone = batch.person.first_phone()
                if phone:
                    info['phone_number'] = phone.number
                email = batch.person.first_email()
                if email:
                    info['email_address'] = email.address

        return info

    def custom_product_autocomplete(self, session, term, **kwargs):
        """
        For the given term, this should return a (possibly empty) list
        of products which "match" the term.  Each element in the list
        should be a dict with "label" and "value" keys.
        """
        raise NotImplementedError("Please define the "
                                  "{}.custom_product_autocomplete() "
                                  "method.".format(__class__.__name__))

    def refresh_row(self, row):
        if not row.product:
            if row.item_entry:
                session = orm.object_session(row)
                # TODO: should do more than just query for uuid here
                product = session.query(model.Product).get(row.item_entry)
                if product:
                    row.product = product
            if not row.product:
                row.status_code = row.STATUS_PRODUCT_NOT_FOUND
                return

        product = row.product
        row.product_upc = product.upc
        row.product_brand = six.text_type(product.brand or "")
        row.product_description = product.description
        row.product_size = product.size
        row.product_weighed = product.weighed
        row.case_quantity = self.get_case_size_for_product(product)

        department = product.department
        row.department_number = department.number if department else None
        row.department_name = department.name if department else None

        cost = product.cost
        row.product_unit_cost = cost.unit_cost if cost else None

        regprice = product.regular_price
        row.unit_price = regprice.price if regprice else None

        # we need to know if total price is updated
        old_total = row.total_price

        # maybe update total price
        if row.unit_price is None:
            row.total_price = None
        elif not row.unit_price:
            row.total_price = 0
        else:
            row.total_price = row.unit_price * row.order_quantity
            if row.order_uom == self.enum.UNIT_OF_MEASURE_CASE:
                row.total_price *= (row.case_quantity or 1)

        # update total price for batch too, if it changed
        if row.total_price != old_total:
            batch = row.batch
            batch.total_price = ((batch.total_price or 0)
                                 + (row.total_price or 0)
                                 - (old_total or 0))

        row.status_code = row.STATUS_OK

    def remove_row(self, row):
        batch = row.batch

        if not row.removed:
            row.removed = True

            if row.total_price:
                batch.total_price = (batch.total_price or 0) - row.total_price

        self.refresh_batch_status(batch)

    def execute(self, batch, user=None, progress=None, **kwargs):
        """
        Default behavior here will simply create a new (proper) Customer Order
        based on the batch contents.  Override as needed.
        """
        batch_fields = [
            'store',
            'id',
            'customer',
            'person',
            'phone_number',
            'email_address',
            'total_price',
        ]

        order = model.CustomerOrder()
        order.created_by = user
        order.status_code = self.enum.CUSTORDER_STATUS_ORDERED
        for field in batch_fields:
            setattr(order, field, getattr(batch, field))

        row_fields = [
            'product',
            'product_upc',
            'product_brand',
            'product_description',
            'product_size',
            'product_weighed',
            'department_number',
            'department_name',
            'case_quantity',
            'order_quantity',
            'order_uom',
            'product_unit_cost',
            'unit_price',
            'discount_percent',
            'total_price',
            'paid_amount',
            'payment_transaction_number',
        ]

        def convert(row, i):
            item = model.CustomerOrderItem()
            item.sequence = i
            item.status_code = self.enum.CUSTORDER_ITEM_STATUS_INITIATED
            for field in row_fields:
                setattr(item, field, getattr(row, field))
            order.items.append(item)

            # attach event
            item.events.append(model.CustomerOrderItemEvent(
                type_code=self.enum.CUSTORDER_ITEM_EVENT_INITIATED,
                user=user))

        self.progress_loop(convert, batch.active_rows(), progress,
                           message="Converting batch rows to order items")

        session = orm.object_session(batch)
        session.add(order)
        session.flush()

        return order
