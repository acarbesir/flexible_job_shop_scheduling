class Order:
    def __init__(self, order_no, customer_name, baca_order_no, customer_due_date, baca_due_date, to_be_planned):
        self.order_no = order_no
        self.customer_name = customer_name
        self.baca_order_no = baca_order_no
        self.customer_due_date = customer_due_date
        self.baca_due_date = baca_due_date
        self.to_be_planned = to_be_planned
