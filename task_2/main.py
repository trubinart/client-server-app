import json


def write_order_to_json(item, quantity, price, buyer, date):
    product = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': quantity
    }

    with open('orders.json', 'r') as file_to_read:
        from_file = file_to_read.read()
        list_to_write = json.loads(from_file)
        list_to_write.append(product)

        with open('orders.json', 'w') as file_to_write:
            file_to_write.write(json.dumps(list_to_write, indent=2))


if __name__ == "__main__":
    write_order_to_json('boots', 23, 4000, 'KENT', '19.08.2021')