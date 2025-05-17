```mermaid
flowchart TD
    A[用户选择Excel文件] --> B[输入日期范围]
    B --> C{有效日期?}
    C -->|是| D[读取生产排程表]
    C -->|否| E[显示错误提示]
    D --> F{文件存在?}
    F -->|是| G[解析第6行日期]
    F -->|否| E
    G --> H[筛选日期范围内数据]
    H --> I[遍历目标列]
    I --> J{值∈2,3,10,16?}
    J -->|是| K{红底色/红文字?}
    J -->|否| I
    K -->|是| L[收集单元格数据]
    K -->|否| I
    L --> M[转换日期格式]
    M --> N[生成结果表格]
    N --> O[自动调整列宽]
    O --> P[保存新Excel文件]
    P --> Q[显示成功提示]
    E --> R[结束流程]
    Q --> R
    
    style A fill:#4CAF50,stroke:#388E3C
    style E fill:#FF5252,stroke:#D32F2F
    style R fill:#9E9E9E,stroke:#616161
    style I fill:#00ACC1,stroke:#00838F