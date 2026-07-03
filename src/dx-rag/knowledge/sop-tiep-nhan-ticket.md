# SOP: Quy trình tiếp nhận và xử lý ticket

## Phân loại và phân công
- Ticket loại **Kỹ thuật** được giao cho **Tổ Kỹ thuật**.
- Ticket loại **Thanh toán** được giao cho **Tổ Kế toán**.
- Ticket loại **Khác** được giao cho **Tổ Chăm sóc Khách hàng (CSKH)**.

## Cam kết thời gian xử lý (SLA)
- Ưu tiên **Cao**: xử lý trong vòng **4 giờ**.
- Ưu tiên **Trung bình**: xử lý trong vòng **24 giờ**.
- Ưu tiên **Thấp**: xử lý trong vòng **72 giờ**.
- Nếu ticket không nêu mức ưu tiên, hệ thống tự suy luận: ticket Kỹ thuật mặc định ưu tiên Cao, các loại khác mặc định Trung bình.

## Trạng thái ticket
Một ticket đi qua các trạng thái: **mới → đang xử lý → hoàn thành** (hoặc **đã hủy**).

## Rào chắn nhập liệu (Poka-yoke)
Số điện thoại khách hàng bắt buộc đúng định dạng Việt Nam (VD: 0901234567 hoặc +84901234567). Ticket có số điện thoại sai sẽ bị từ chối ngay tại đầu nguồn.
