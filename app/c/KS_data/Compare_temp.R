foreground <- c(0,1,2,3,4,5)
background <- c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23)
result_tw <- ks.test(foreground, background)
result_tw$statistic # 0.7142857
result_tw$p.value # 0.01709861

foreground <- c(0, 2, 4, 6, 8, 10, 12, 14, 16, 18)
background <- c(1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49)
result_tw <- ks.test(foreground, background)
result_tw$statistic # 0.64
result_tw$p.value # 0.003018225

fg <- c(0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38)
bg <- c(1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99)
result_tw <- ks.test(fg, bg)
result_tw$statistic # 0.62
result_tw$p.value # 1.20284e-05

ks.test
