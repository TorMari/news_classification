# Audit Summary — Lab 5 (Split + leakage checks)

## Розподіл класів у train/val/test 
Counts:
             train  val  test
category_id                  
0.0            147   31    32
1.0            144   31    32
2.0            144   30    32
3.0            144   30    32

Percent:
             train    val  test
category_id                    
0.0          25.39  25.41  25.0
1.0          24.87  25.41  25.0
2.0          24.87  24.59  25.0
3.0          24.87  24.59  25.0

## Розподіл довжин тексту по сплітах
          mean  median      p5      p95
train  1367.01  1258.0  420.60  2645.70
val    1438.00  1296.0  493.85  2771.35
test   1500.50  1359.5  536.40  2941.65

## Leakage checks

### Duplicate leakage
* exact duplicates train∩test: 0
* exact duplicates train∩val: 0
* exact duplicates val∩test: 0

### Near-duplicate leakage
Suspicious pairs train vs test: 6

### Template / metadata leakage
Suspicious rows found: 0
Rows containing class names: 2

### Time leakage
                             train_min                  train_max  \
category_id                                                         
0.0          2026-01-14T14:52:00+02:00  2026-02-05T06:07:00+02:00   
1.0          2026-02-02T10:45:00+02:00  2026-02-10T22:11:00+02:00   
2.0          2026-02-05T10:36:00+02:00  2026-02-11T14:37:00+02:00   
3.0          2026-02-03T11:58:00+02:00  2026-02-10T19:42:00+02:00   

                               val_min                    val_max  \
category_id                                                         
0.0          2026-02-05T10:47:00+02:00  2026-02-09T17:47:00+02:00   
1.0          2026-02-11T00:41:00+02:00  2026-02-12T13:27:00+02:00   
2.0          2026-02-11T14:43:37+02:00  2026-02-12T12:21:00+02:00   
3.0          2026-02-10T19:50:00+02:00  2026-02-11T20:44:00+02:00   

                              test_min                   test_max  leakage_ok  
category_id                                                                    
0.0          2026-02-10T13:01:00+02:00  2026-02-13T13:47:54+02:00        True  
1.0          2026-02-12T13:39:31+02:00  2026-02-13T13:22:00+02:00        True  
2.0          2026-02-12T12:38:59+02:00  2026-02-13T13:43:00+02:00        True  
3.0          2026-02-11T22:01:00+02:00  2026-02-13T14:00:11+02:00        True  
