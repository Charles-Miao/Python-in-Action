```mermaid
flowchart TD
    A[用户点击开始按钮] --> B[读取Excel获取PKID列表]
    B --> C{是否成功读取?}
    C --> |是| D[连接MDOS应用]
    C --> |否| E[记录错误日志]
    D --> F{是否连接成功?}
    F --> |是| G[定位主窗口和控件]
    F --> |否| E
    G --> H[点击CBR按钮]
    H --> I[进入搜索界面]
    I --> J[循环处理每个PKID]
    J --> K[输入PKID并搜索]
    K --> L{是否找到数据?}
    L --> |是| M[勾选复选框并提交]
    L --> |否| N[记录已提交状态]
    M --> O[确认提交弹窗]
    O --> P{是否确认成功?}
    P --> |是| Q[记录提交成功]
    P --> |否| E
    Q --> R[等待下一个PKID]
    R --> J
    N --> R
    E --> S[结束流程]
    Q --> S
    N --> S
    S --> T[程序结束]
    
    style A fill:#4CAF50,stroke:#388E3C
    style E fill:#FF5252,stroke:#D32F2F
    style S fill:#9E9E9E,stroke:#616161