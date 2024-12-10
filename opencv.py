import cv2


def edge_points(file_path, output_path, scale=1):

    # 画像を読み込む
    img = cv2.imread(file_path)

    # グレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ガウシアンフィルターをかける
    gauss = cv2.GaussianBlur(gray, (5, 5), 0)

    # 2値化する
    thres = cv2.threshold(gauss, 140, 255, cv2.THRESH_BINARY)[1]

    # 輪郭のみを検出する
    cons = cv2.findContours(thres, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]

    # 面積の最小値（線の内側の座標）を除外
    min_contour = min(cons, key=cv2.contourArea)
    cons = [contour for contour in cons if contour is not min_contour]

    # 最大の輪郭を除外するため、リストから削除
    max_contour = max(cons, key=cv2.contourArea)
    contours = [contour for contour in cons if contour is not max_contour]

    # 輪郭を描画する
    for con in contours:
        cv2.polylines(img, con, True, (0, 255, 0), 5)
    cv2.imshow("result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    points = []
    for con in contours:
            for point in con:
                # point[0]はx, point[1]はy座標
                x, y = point[0]
                points.append((x, y))
        
    # 必要のない値を削除する処理
    optimized_points = []
    n = len(points)

    i = 0
    while i < n:
        current_run = [points[i]]
        while i + 1 < n and (points[i][0] == points[i + 1][0] or points[i][1] == points[i + 1][1]):
            current_run.append(points[i + 1])
            i += 1
        if len(current_run) > 1:
            # 始端と終端だけ追加
            optimized_points.append(current_run[0])
            optimized_points.append(current_run[-1])
        else:
            # 連続していない場合そのまま追加
            optimized_points.append(points[i])
        i += 1

    # 最適化されたポイントを保存
    with open(output_path, 'w') as output_file:
        for x, y in optimized_points:
            x = x * scale
            y = y * scale
            output_file.write(f"{x},{y}\n")

# 使用例
input_image = "S.jpg"  # 入力ファイル
output_file = "S.txt"  # 出力ファイル

edge_points(input_image, output_file, 0.25)