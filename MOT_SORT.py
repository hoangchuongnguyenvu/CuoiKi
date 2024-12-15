import streamlit as st

def main():
    st.title("SORT - Simple Online and Realtime Tracking")
    
    # 1. Giới thiệu
    st.header("1. Giới thiệu")
    
    # 1.1. Tổng quan
    st.subheader("1.1. Tổng quan") 
    st.markdown("""
    - **SORT** (Simple Online and Realtime Tracking) là một thuật toán theo dõi nhiều đối tượng (Multi-Object Tracking - MOT) 
    được phát triển với mục tiêu đơn giản hóa quá trình tracking nhưng vẫn đảm bảo hiệu suất cao cho ứng dụng thời gian thực.
    SORT được thiết kế để giải quyết bài toán theo dõi đa đối tượng một cách hiệu quả và đơn giản, phù hợp cho các ứng dụng 
    thực tế đòi hỏi xử lý thời gian thực như giám sát an ninh, phân tích giao thông hay phân tích hành vi.

    - **Hoàn cảnh ra đời:**
    Trong bối cảnh các thuật toán tracking đang ngày càng trở nên phức tạp, cộng đồng Computer Vision cần một giải pháp đơn giản 
    nhưng vẫn đảm bảo hiệu quả cho các ứng dụng thời gian thực.

        - *Thời điểm công bố:* Năm 2016

        - *Nơi công bố:* IEEE International Conference on Image Processing (ICIP)

        - *Tác giả:* Alex Bewley và các cộng sự

        - *Tham khảo:* [Simple Online and Realtime Tracking](https://arxiv.org/abs/1602.00763)

    - **Đặc điểm nổi bật**:
        - Tốc độ xử lý cực nhanh: >260 FPS trên CPU đơn nhân, vượt trội so với các phương pháp cùng thời
        - Kiến trúc đơn giản: kết hợp Kalman Filter và Hungarian Algorithm một cách hiệu quả
        - Độ chính xác (MOTA) cạnh tranh với các phương pháp phức tạp hơn nhiều
        - Không yêu cầu GPU hay deep learning cho quá trình tracking
        - Dễ dàng tích hợp với bất kỳ object detector nào
        - Mã nguồn mở và được cộng đồng phát triển mạnh mẽ
    """)

    # Hiển thị bảng so sánh
    col1, col2, col3 = st.columns([1,10,1])
    with col2:
        st.image('UIUX/SORT/bsbsbs.png', caption='Bảng so sánh hiệu suất của SORT với các phương pháp khác')

    # Thêm phần nhận xét về hiệu suất
    st.markdown("""
    - **Phân tích hiệu suất của SORT**:
        - **Độ chính xác cao**: 
            - MOTA (Multiple Object Tracking Accuracy) đạt 33.4%, nằm trong top các phương pháp tốt nhất
            - MOTP (Multiple Object Tracking Precision) đạt 72.1%, cho thấy độ chính xác về vị trí rất tốt
        
        - **Hiệu quả trong xử lý thời gian thực**:
            - Là phương pháp Online (xử lý theo thời gian thực)
            - Hiệu suất cạnh tranh với cả các phương pháp Batch (xử lý offline)
        
        - **Ưu điểm nổi bật**:
            - FAF (False Alarm per Frame) thấp: chỉ 1.3%, giảm thiểu cảnh báo sai
            - ML (Mostly Lost) thấp nhất: 30.9%, cho thấy khả năng duy trì track tốt
            - FP (False Positives) thấp: 7318, ít nhận diện sai
            - FN (False Negatives) ở mức tốt: 32615, cân bằng giữa bỏ sót và nhận diện sai
    """)

    # 1.2. Chi tiết thuật toán
    st.subheader("1.2. Chi tiết thuật toán")
    
    # Hiển thị hình ảnh minh họa tổng quan về SORT
    col1, col2, col3 = st.columns([1,10,1])
    with col2:
        st.image('UIUX/SORT/image.png', caption='Sơ đồ tổng quan thuật toán SORT')
    
    st.markdown("""
    ### Thuật toán SORT hoạt động qua các bước chính:

    #### 1. Object Detection
    - Sử dụng một detector bên ngoài (như YOLO, SSD, Faster R-CNN) để phát hiện đối tượng trong mỗi frame
    - Mỗi detection bao gồm bounding box và điểm số tin cậy
    - Detector có thể được tùy chọn dựa trên yêu cầu về tốc độ và độ chính xác
    - Output của detector sẽ là danh sách các bounding box với format [x1, y1, x2, y2, score]

    #### 2. State Estimation với Kalman Filter
    - Dự đoán vị trí của đối tượng trong frame tiếp theo
    - Sử dụng mô hình chuyển động tuyến tính
    - State vector bao gồm 7 thành phần: [u, v, s, r, u̇, v̇, ṡ]
        - u, v: tọa độ tâm bbox
        - s: diện tích
        - r: tỷ lệ khung hình
        - u̇, v̇, ṡ: vận tốc tương ứng
    - Kalman Filter thực hiện hai bước:
        - Predict: Dự đoán state mới dựa trên mô hình chuyển động
        - Update: Cập nhật state dựa trên measurement mới

    #### 3. Data Association với Hungarian Algorithm
    - Liên kết các detection mới với các track hiện có
    - Sử dụng IoU (Intersection over Union) làm metric đo độ tương đồng
    - Quy trình association:
        1. Tính ma trận IoU giữa tất cả các cặp detection-track
        2. Áp dụng Hungarian Algorithm để tìm assignment tối ưu
        3. Lọc bỏ các assignment có IoU thấp hơn ngưỡng
    - Kết quả cho ra ba tập:
        - Matched tracks: Các cặp detection-track được ghép
        - Unmatched detections: Detections không được ghép với track nào
        - Unmatched tracks: Tracks không được ghép với detection nào

    #### 4. Track Management
    - Quản lý vòng đời của các track trong hệ thống
    - Các hoạt động chính:
        1. Khởi tạo track mới:
            - Tạo từ unmatched detections
            - Khởi tạo Kalman Filter với state vector ban đầu
        2. Cập nhật track hiện có:
            - Update Kalman Filter với matched detections
            - Cập nhật số frame liên tiếp track được/mất detection
        3. Xóa track:
            - Xóa track khi không được cập nhật trong max_age frames
            - Hoặc track có chất lượng thấp (ít hits)
                
    Mỗi bước trong thuật toán đều được thiết kế để đơn giản và hiệu quả, tập trung vào việc xử lý realtime. 
    Việc sử dụng Kalman Filter cho prediction và Hungarian Algorithm cho data association tạo nên một giải pháp 
    tracking đơn giản nhưng mạnh mẽ.
    """)

    col1, col2, col3 = st.columns([1,10,1])
    with col2:
        st.image('5.png', caption='Minh họa bằng frame thực tế')


    # 1.3. Ví dụ minh họa
    st.subheader("1.3. Ví dụ minh họa")
    
    st.markdown("""
    ### Demo SORT Algorithm
    
    Dưới đây là ví dụ minh họa việc áp dụng thuật toán SORT để theo dõi đối tượng trong video.
    Video demo thể hiện các bước trong quy trình hoạt động của SORT:
    
    - Phát hiện đối tượng bằng YOLOv8
    - Tracking đối tượng qua các frame
    - Gán ID và theo dõi quỹ đạo chuyển động
    """)
    
    # Tạo 2 cột để căn giữa video
    col1, col2, col3 = st.columns([1,10,1])
    
    with col2:
        # Hiển thị video demo trực tiếp từ file
        st.video('UIUX/SORT/output_tracked.mp4')  # Thay đổi tên file video của bạn
    
    st.markdown("""
    ### Giải thích kết quả:
    
    - **Bounding box màu**: Khung theo dõi đối tượng
    - **ID**: Số định danh duy nhất cho mỗi đối tượng
    - **Tọa độ**: Vị trí tâm của đối tượng
    - **Số lượng**: Tổng số đối tượng đang được theo dõi
    """)
    
    # 3. Thảo luận về các trường hợp thách thức
    st.header("3. Thảo luận về các trường hợp thách thức")
    
    # Tạo tabs cho các trường hợp
    tabs = st.tabs(["Background Clutters",])
    
    # Tab Background Clutters
    with tabs[0]:
        st.subheader("Background Clutters (Nền phức tạp)")
        
        # Tạo 2 cột cho video
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Video gốc")
            st.video('UIUX/SORT/walking_output.mp4')
            
        with col2:
            st.markdown("### SORT tracking")
            st.video('output_tracked (1).mp4')
            
        st.markdown("""
    ### Giải thích cơ chế Tracking trong SORT

    Dựa vào code và hiểu biết về thuật toán SORT, ta có thể giải thích nguyên nhân tại sao có sự khác biệt trong khả năng mất và khôi phục tracking:

    **1. Trường hợp có thể khôi phục tracking:**
    - Khi một đối tượng bị mất tracking trong thời gian ngắn (ví dụ bị che khuất tạm thời hoặc nhiễu) nhưng sau đó xuất hiện lại ở vị trí gần với dự đoán của Kalman Filter
    - Điều này xảy ra vì SORT sử dụng Kalman Filter để dự đoán vị trí tiếp theo của đối tượng dựa trên các thông số như vận tốc và hướng di chuyển trước đó
    - Nếu đối tượng xuất hiện lại trong khoảng thời gian max_age (trong code là 20 frames) và có IoU với bbox dự đoán cao hơn iou_threshold (0.3), SORT sẽ gán lại ID cũ cho đối tượng

    **2. Trường hợp không thể khôi phục tracking:**
    - Khi đối tượng xuất hiện lại ở vị trí quá khác so với dự đoán của Kalman Filter
    - Khi thời gian mất dấu vượt quá max_age frames (20 frames trong code)
    - Khi đối tượng có sự thay đổi đột ngột về hướng di chuyển hoặc vận tốc khiến dự đoán của Kalman Filter không còn chính xác
    - Khi có nhiều đối tượng tương tự nhau ở gần nhau, việc gán ID có thể bị nhầm lẫn
    - Ngoài ra, với môi trường phức tạp như "Background Clutters" thì bounding box từ detector có thể bị nhiễu hoặc không ổn định.
    """)

    st.markdown("""
    ### Phân tích trường hợp cụ thể

    **Trường hợp 1: ID 1 - Khôi phục tracking thành công**
    """)
    image1 = "frame_0049.png"
    image2 = "frame_0050.png"
    image3 = "frame_0055.png"


# Sử dụng cột để hiển thị ảnh cạnh nhau
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(image1, caption="Frame 49", use_column_width=True)

    with col2:
        st.image(image2, caption="Frame 50", use_column_width=True)

    with col3:
        st.image(image3, caption="Frame 55", use_column_width=True)
    st.markdown("""
    **Diễn biến sự kiện:**
    - Frame 49: Vẫn giữ được tracking
    - Frame 50: Bị mất tracking
    - Frame 55: Khôi phục lại được ID ban đầu

    **Phân tích:**
    - Nguyên nhân chính: Kalman Filter dự đoán dựa trên vận tốc và hướng di chuyển
    - Frame 49: Velocity = 3.39
    - Frame 50: Velocity tăng đột ngột lên 10.12 → Dự đoán Kalman Filter không chính xác
    - Frame 51-55: Velocity ổn định (3.3-3.7) → Phù hợp với dự đoán → Khôi phục tracking thành công

    **Trường hợp 2: ID 2 → ID 8 - Không thể khôi phục tracking**
    """)
    image1 = "frame_0057.png"
    image2 = "frame_0063.png"
    image3 = "frame_0070.png"


# Sử dụng cột để hiển thị ảnh cạnh nhau
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(image1, caption="Frame 57", use_column_width=True)

    with col2:
        st.image(image2, caption="Frame 63", use_column_width=True)

    with col3:
        st.image(image3, caption="Frame 70", use_column_width=True)
    st.markdown("""
    **Diễn biến sự kiện:**
    - Frame 57: Đối tượng vẫn giữ ID là 2 
    - Frame 63: Chuyển sang ID là 8 
    - Frame 70: Vẫn giữu ID là 8 cho đến các frame này rồi mất hẳn về sau.          
    
    **Phân tích:**
    - Không phải do Track Management (max_age = 20 frames)
    - Quá trình bị mất tracking
    - Nguyên nhân: Có 4 đối tượng được YOLO detect trên cùng một đối tượng
    - Hệ quả: Gán ID bị nhầm lẫn → ID thay đổi từ 2 thành 8 và rồi sau đó với ảnh hưởng của "Background Clutters" dẫn đến detector không thể phát hiện bounding box
                làm mất đi tracking.
    """)
    


if __name__ == "__main__":
    main()