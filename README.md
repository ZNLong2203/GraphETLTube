# Graph ETL for metadata

## Giới thiệu chung
- Sau khi data từ postgresql được lấy về, em sẽ thực hiện ETL để chuyển dữ liệu từ dạng đồ thị
sang dạng file json để dễ dàng truy vấn trên elasticsearch.
- Luồng ETL sẽ được thực hiện như sau:
    - Đọc dữ liệu từ postgresql
    - Xử lý data bằng python
    - Chuyển dữ liệu đã được xử lý bằng spark sang elasticsearch

## Các file thành phần
- `create_data.py`: file chứa các hàm để tạo dữ liệu mẫu cho postgresql
- `etl.py`: file chứa các hàm để thực hiện ETL
- `elastic_search.py`: file chứa các hàm để thực hiện việc tạo index và insert dữ liệu vào elasticsearch
- `docker-compose.yml`: file chứa cấu hình để chạy elasticsearch và postgresql
- `data.json`: file chứa dữ liệu đã được xử lý (bình thường sẽ được lưu trong s3)

## Một số ý tưởng chính để xử lý dữ liệu
- Graph view

![graphView.png](img%2FgraphView.png)
- Table view

![tableView.png](img%2FtableView.png)

- Ý tưởng chính: 

1. Sau khi thấy hai loại view trên, đối với graph view, em nhận thấy từ một node, ta có thể tìm ra các node khác mà nó liên kết với nhau. Vì vậy, em sẽ chuyển dữ liệu từ postgresql sang dạng đồ thị, mỗi node sẽ là một bảng, mỗi cạnh sẽ là một quan hệ giữa các bảng
và sẽ có một bảng node chính để lưu thông tin về id, name, relationship các node khác để tiện cho việc truy vấn (performance thì
em nghĩ là sẽ tùy loại dạng dữ liệu mà sẽ tương tự việc đánh index từng node, ưu điểm là cách này sẽ cần ít bảng hơn)
2. Khi chọn một node, thì em nhận ra sẽ có thể có nhiều đường đi tới nó như trên ảnh graph view, nên sử dụng backtracking để sinh kế tiếp, liệt kê ra các đường đi tới node đó,
và rồi sử dụng "set" để lọc các node trùng nhau và sort theo thứ tự id node tăng dần
3. Kế tiếp em nhận thấy từ các node trên tới node được chọn có thể sẽ có relationship "optional" nên em sẽ query để check và loại bỏ các node không cần thiết
4. Serializer data để chuyển sang dạng json
5. Cuối cùng là chuyển dữ liệu đã được xử lý sang elasticsearch và tạo index

![ESGraphETL.png](img%2FESGraphETL.png)