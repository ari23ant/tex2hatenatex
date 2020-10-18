数式テスト
==========
この.mdファイルは数式テストファイル

----------------------------------------------------------------------------

斜方投射
--------
「斜方投射」というとちょっと難しい印象ですが、だたのボールを斜めに投げる放物線運動です。高校物理の範囲ですが、少し難しくするために空気抵抗を考慮します。

**したがってここでは、真のモデル${f_t}^{perfect}$を空気抵抗ありのモデル式、シミュレーションモデル$f_t$を空気抵抗なしのモデル式とし、カルマンフィルタを使って真値を予測することを目的とします。**

### 空気抵抗あり
質量$m$のボールを角度$\theta$で投げたときのボールのxy座標を式で求める。初速は$v_0$で、初期位置は$(0, 0)$、空気抵抗は速度に比例し$r$とする。なお、ボールの大きさは考えない。

|項目|内容|
|:--:|:--------:|
|質量|$m$[kg]|
|初速|$v_0$[m/s]|
|初期座標|$(0, 0)$[m]|
|投射角度|$\theta$[rad]|
|空気抵抗|$r$[kg/s]|
|重力加速度|$g$[m/s^2]|

座標系は次の通り。

![斜方投射のxy座標](xy_projectile_motion.png '斜方投射のxy座標')

x軸とy軸の運動方程式は以下のように書ける。

$$
\begin{align}
m a_x &= - r v_x \\
m a_y &= - m g - r v_y
\end{align}
$$

両辺に$\times \frac{1}{m}$する。

$$
\begin{align}
a_x &= - \frac{r}{m} v_x \\
a_y &= - g - \frac{r}{m} v_y
\end{align}
$$

上式より、速度は以下のように書ける。

$$
\begin{align}
v_x &= v_0 \cos\theta \ \exp \biggl( -\frac{r}{m} t \biggr) \\
v_y &= (v_0 \sin\theta + gt) \ \exp \biggl( -\frac{r}{m} t \biggr) - \frac{m}{r} g
\end{align}
$$

よって、x座標とy座標は以下となる。

$$
\begin{align}
x &= \frac{m v_0}{r} \biggl( 1 - \exp \Bigl( -\frac{r}{m} t \Bigr) \biggr) \cos\theta \\
y &= \frac{m}{r} \biggl\{ \biggl(v_0 \sin\theta + \frac{m}{r} g \biggr) \biggl( 1 - \exp \Bigl( -\frac{r}{m} t \Bigr) \biggr) - gt \biggr\}
\end{align}
$$


状態空間モデル
--------------
今度は、空気抵抗なしのシミレーションモデルを使って、状態空間モデルを立ててみます。

**線形・ガウス状態空間モデル**

$$
\begin{align}
\boldsymbol{x}_t &= F_t \boldsymbol{x}_{t-1} + G_t \boldsymbol{v}_t \qquad \boldsymbol{v}_t \sim N(\boldsymbol{0}, Q_t)\\
\boldsymbol{y}_t &= H_t \boldsymbol{x}_t + \boldsymbol{w}_t \qquad \quad \ \boldsymbol{w}_t \sim N(\boldsymbol{0}, R_t)
\end{align}
$$

### システムモデル
状態変数をx軸の位置、速度、加速度と、y軸の位置、速度、加速度を含んだベクトルとする。つまり、$\boldsymbol{x}_t=[x_t, \dot{x}_t, \ddot{x}_t, y_t, \dot{y}_t, \ddot{y}_t]^{\prime}$とおく。  
簡単のためシステムノイズを省略すると、以下のように書ける。

$$
\begin{align}
\boldsymbol{x}_t &= F_t \boldsymbol{x}_{t-1}  \\

\Leftrightarrow

\left[
  \begin{array}{c}
    x_t  \\
    \dot{x}_t  \\
    \ddot{x}_t  \\
    y_t  \\
    \dot{y}_t  \\
    \ddot{y}_t  \\
  \end{array}
\right]

&=

\begin{bmatrix}
1 & \Delta t & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 & 0  \\
0 & 0 & 1 & 0 & 0 & 0  \\
0 & 0 & 0 & 1 & \Delta t & \frac{(\Delta t)^2}{2}  \\
0 & 0 & 0 & 0 & 1 & \Delta t  \\
0 & 0 & 0 & 0 & 0 & 1  \\
\end{bmatrix}

\left[
  \begin{array}{c}
    x_{t-1}  \\
    \dot{x}_{t-1}  \\
    \ddot{x}_{t-1}  \\
    y_{t-1}  \\
    \dot{y}_{t-1}  \\
    \ddot{y}_{t-1}  \\
  \end{array}
\right]
\end{align}
$$

### 観測モデル
今回の系では、x軸の位置とy軸の位置が観測できるとする。つまり、$\boldsymbol{y}_t=[x_t, y_t]^{\prime}$とおく。  
簡単のため観測ノイズを省略すると、以下のように書ける。

$$
\begin{align}
\boldsymbol{y}_t &= H_t \boldsymbol{x}_{t}  \\

\Leftrightarrow

\left[
  \begin{array}{c}
    x_t  \\
    y_t  \\
  \end{array}
\right]

&=

\begin{bmatrix}
1 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 & 0  \\
\end{bmatrix}

\left[
  \begin{array}{c}
    x_t  \\
    \dot{x}_t  \\
    \ddot{x}_t  \\
    y_t  \\
    \dot{y}_t  \\
    \ddot{y}_t  \\
  \end{array}
\right]
\end{align}
$$


----------------------------------------------------------------------------

線形・ガウス状態空間モデル
--------------------------
以前の記事で、データ同化の基本である状態空間モデルを扱った。

[データ同化｜ざっくり解説](https://ari23.hatenablog.com/entry/da-easy-explanation)

上記の記事では、システムモデルと観測モデルの線形性や、システムノイズや観測ノイズの確率分布に言及していない。

カルマンフィルタでは、システムノイズと観測モデルは線形モデルであり、システムノイズや観測ノイズはガウス分布（正規分布）に従うとする。つまり、状態空間モデルを以下のように書くことができる。

$$
\begin{align}
\boldsymbol{x}_t &= F_t \boldsymbol{x}_{t-1} + G_t \boldsymbol{v}_t \qquad \boldsymbol{v}_t \sim N(\boldsymbol{0}, Q_t)\\
\boldsymbol{y}_t &= H_t \boldsymbol{x}_t + \boldsymbol{w}_t \qquad \quad \ \boldsymbol{w}_t \sim N(\boldsymbol{0}, R_t)
\end{align}
$$

各変数の説明と形は以下の通り。ただし、※がついた名称は一般的ではない可能性があることに注意されたい。

|変数|次元|説明|
|:--:|:---|:---|
|$\boldsymbol{x}_t$|$k$|時刻$t$の状態変数（ベクトル）|
|$\boldsymbol{x}_{t-1}$|$k$|時刻$t-1$の状態変数（ベクトル）|
|$F_t$|$k \times k$|時刻$t$のシステム行列※または遷移行列|
|$G_t$|$k \times m$|時刻$t$のシステムノイズ行列※|
|$\boldsymbol{v}_t$|－|時刻$t$のガウス分布$N(\boldsymbol{0}, Q_t)$に従うシステムノイズ|
|$Q_t$|$m \times m$|時刻$t$のシステムモデルの分散共分散行列|
|$\boldsymbol{y}_t$|$\ell$|時刻$t$の観測値（ベクトル）|
|$H_t$|$\ell \times k$|時刻$t$の観測行列※|
|$\boldsymbol{w}_t$|－|時刻$t$のガウス分布$N(\boldsymbol{0}, Q_t)$に従う観測ノイズ|
|$R_t$|$\ell \times \ell$|時刻$t$の観測モデルの分散共分散行列|

分散共分散行列とは、分散の概念を一次元から多次元（多変量）の確率変数に拡張し行列で表現したものである。
以下に、ガウス分布（正規分布）$N(\boldsymbol{\mu}, \boldsymbol{\Sigma})$に従う二次元確率変数$\boldsymbol{x}$の確率密度関数$f(\boldsymbol{x})$を示す。

$$
f(\boldsymbol{x}) = \frac{1}{\sqrt{(2\pi)^2 |\Sigma|}} \exp \biggl( -\frac{1}{2} (\boldsymbol{x} - \boldsymbol{\mu})^{\prime} \Sigma^{-1} (\boldsymbol{x} - \boldsymbol{\mu}) \biggr)
$$

参考として、一次元の確率分布を以下に示す。

$$
f(x) = \frac{1}{\sqrt{2\pi \sigma^{2}}} \exp \biggl( -\frac{(x-m)^{2}}{2 \sigma^{2}} \biggr)
$$


### 制御理論の場合
制御理論、特に現代制御では状態空間モデルを、例えば以下のように表すことが多いと思います（MATLABの[カルマンフィルター](https://jp.mathworks.com/discovery/kalman-filter.html)を参考）。

$$
\begin{align}
x[n+1] &= Ax[n] + Bu[n] + Gw[n] \\
y_v[n] &= Cx[n] + v[n]
\end{align}
$$

変数の違いはもちろんですが、一番の違いは入力の$Bu[n]$です。私は制御もかじっているせいか、この$Bu[n]$によってかなり混乱しました。しかし本質はまったく同じで、この入力を状態変数$\boldsymbol{x}$に入れてしまえば、最初に出した状態空間モデルと一致します。


予測とフィルタ
--------------
カルマンフィルタのアルゴリズムに入る前に、予測とフィルタ（濾波ともいう）の考えを導入する。

データ同化は、モデルと観測値をうまく馴染ませる技術であると説明した。

[データ同化｜ざっくり解説](https://ari23.hatenablog.com/entry/da-easy-explanation)

今、時刻$t$において、状態変数$\boldsymbol{x}_t$を予測することを考えたい。  
このとき、手元には時刻$1$から$t-1$までの（時刻$t$以外の）観測値があり、これを$\boldsymbol{y}_{1:t-1}$と書くことにする。$\boldsymbol{x}_t$の確率（密度）は、$\boldsymbol{y}_{1:t-1}$を条件とする、条件確率として以下のように書ける。

$$
p(\boldsymbol{x}_t | \boldsymbol{y}_{1:t-1})
$$

これを予測分布と呼ぶ。

次に、同じく時刻$t$のときに観測値$\boldsymbol{y}_{t}$が追加されたとする。新たに情報が追加され、$\boldsymbol{x}_t$の条件確率が更新される。

$$
p(\boldsymbol{x}_t | \boldsymbol{y}_{1:t})
$$

これをフィルタ分布と呼ぶ。

カルマンフィルタをはじめとする、逐次ベイズフィルタでは、この（一期先）予測ステップとフィルタステップ（更新ステップともいう）を交互に操作して分布を求める。以下は、この予測とフィルタを図示したものである。

![予測とフィルタ](prediction_update.png '予測とフィルタ')

**ここでの「分布を求める」とは、各ステップでのガウス分布の平均と分散共分散行列を求めることを意味する。つまり、推定値はフィルタステップで得た平均値である。**

また、フィルタステップでは観測値が追加され、より真値に近い分布に更新されるので、分散がその分だけ小さくなるイメージを持てば良い。

ところで、以下の分布は全区間での観測値を使って求める時刻$t$での分布であり、これを平滑化分布と呼ぶが、ここでは扱わない。

$$
p(\boldsymbol{x}_t | \boldsymbol{y}_{1:T})
$$

以上を次の表でまとめる。

|分布名|表記|観測値の区間|
|:----:|:---|:-----------|
|予測分布| $p(\boldsymbol{x}_t \mid \boldsymbol{y}_{1:t-1})$ |1ステップ前まで|
|フィルタ分布| $p(\boldsymbol{x}_t \mid \boldsymbol{y}_{1:t})$ |今のステップまで|
|平滑化分布| $p(\boldsymbol{x}_t \mid \boldsymbol{y}_{1:T})$ |全区間|


カルマンフィルタ
----------------
カルマンフィルタのアルゴリズムは次の通り。なお、${F_t}^{\prime}$は$F_t$の転置行列を表す。参考として、線形・ガウス状態空間モデルも再掲する。

**線形・ガウス状態空間モデル（再掲）**

$$
\begin{align}
\boldsymbol{x}_t &= F_t \boldsymbol{x}_{t-1} + G_t \boldsymbol{v}_t \qquad \boldsymbol{v}_t \sim N(\boldsymbol{0}, Q_t)\\
\boldsymbol{y}_t &= H_t \boldsymbol{x}_t + \boldsymbol{w}_t \qquad \quad \ \boldsymbol{w}_t \sim N(\boldsymbol{0}, R_t)
\end{align}
$$

<br>

**カルマンフィルタアルゴリズム**

＜初期条件＞  
$\boldsymbol{x}_{0|0}$を初期の状態変数、$V_{0|0}$を初期の状態変数の分散共分散行列とし、時刻$t=1, 2, ..., T$に対して、次の操作を行う。

＜一期先予測＞  
$$
\begin{align}
\boldsymbol{x}_{t|t-1} &= F_t \boldsymbol{x}_{t-1|t-1} + a[z] \\
V_{t|t-1} &= F_t V_{t-1|t-1} {F_t}^{\prime} + G_t Q_t {G_t}^{\prime}
\end{align}
$$

＜フィルタ＞  
$$
\begin{align}
\boldsymbol{e}_t &= \boldsymbol{y}_t - H_t \boldsymbol{x}_{t|t-1} \\
D_{t|t-1} &= H_t V_{t|t-1} {H_t}^{\prime} + R_t \\
K_t &= V_{t|t-1} {H_t}^{\prime} {D_{t|t-1}}^{-1} \\
\boldsymbol{x}_{t|t} &= \boldsymbol{x}_{t|t-1} + K_t \boldsymbol{e}_t \\
V_{t|t} &= V_{t|t-1} - K_t H_t V_{t|t-1}
\end{align}
$$

各変数の説明は以下の通り。

|変数|説明|
|:--:|:---|
|$\boldsymbol{x}_{t \mid t-1}$|時刻$t-1$までの観測値で推定した時刻$t$の推定値、または時刻$t$の予測分布の平均ベクトル|
|$V_{t \mid t-1}$|時刻$t-1$までの観測値で推定した時刻$t$の推定値の誤差の分散、または時刻$t$の予測分布の分散共分散行列|
|$\boldsymbol{e}_t$|時刻$t$の観測値と予測ステップでの推定値から得られるであろう観測値との誤差、または観測残差（イノベーションという）|
|$D_{t \mid t-1}$|観測残差の分散共分散行列|
|$K_t$|最適カルマンゲイン|
|$\boldsymbol{x}_{t \mid t}$|観測値が追加され更新した時刻$t$での推定値、または時刻$t$のフィルタ分布の平均ベクトル|
|$V_{t \mid t}$|観測値が追加され更新した時刻$t$での予測値の誤差の分散、または時刻$t$のフィルタ分布の分散共分散行列|


カルマンフィルタでは原則、この一期先予測とフィルタの操作を交互に繰り返して、状態変数の平均ベクトルと分散共分散行列を求めながら、真値に近い値を推定する。その様子を図示したものは以下の通り。

![カルマンフィルタの予測とフィルタ](kf_prediction_update.png 'カルマンフィルタの予測とフィルタ')

例えば、時刻$t=2$での予測分布は$p(\boldsymbol{x}_{2}|\boldsymbol{y}_{1}) \sim N(\boldsymbol{x}_{2|1}, V_{2|1})$であり、フィルタ分布は$p(\boldsymbol{x}_{2}|\boldsymbol{y}_{2}) \sim N(\boldsymbol{x}_{2|2}, V_{2|2})$であることを示す。


アルゴリズムの導出
------------------
カルマンフィルタのアルゴリズムとその導出については、以下の記事を参考にされたい[^導出]。

[^導出]: 紹介した記事がとても素晴らしいため、自分で書くのはやめて、その分各変数の説明を丁寧に書きました。

- [シンプルなモデルとイラストでカルマンフィルタを直観的に理解してみる](https://qiita.com/MoriKen/items/0c80ef75749977767b43)  
  カルマンフィルタのイメージを図で丁寧に書かれていて、感動しました。  
  特に一次元と多次元で比較した表が非常にわかりやすいです。


尤度
----
カルマンフィルタなどデータ同化を扱うときに最も難しいのは、真値がわからない状態でノイズなどのパラメタを設定することである。このとき、パラメタ設定の指標として尤度を使うのが一般的である。

尤度とは全区間の観測値の同時確率であり、$p(\boldsymbol{y}_{1:T})$と表現できる。これを乗法定理$p(\boldsymbol{a}, \boldsymbol{b}) = p(\boldsymbol{a}|\boldsymbol{b})p(\boldsymbol{b})$を使うと、以下のように書き下せる。

$$
\begin{align}
p(\boldsymbol{y}_{1:T}) &= p(\boldsymbol{y}_T, \boldsymbol{y}_{T-1}, ..., \boldsymbol{y}_1) \\
&= p(\boldsymbol{y}_T|\boldsymbol{y}_{1:T-1}) p(\boldsymbol{y}_{1:T-1}) \\
&= p(\boldsymbol{y}_T|\boldsymbol{y}_{1:T-1}) p(\boldsymbol{y}_{T-1}|\boldsymbol{y}_{1:T-2}) p(\boldsymbol{y}_{1:T-2}) \\
&= \prod_{t=1}^{T}p(\boldsymbol{y}_t|\boldsymbol{y}_{1:t-1})
\end{align}
$$

$p(\boldsymbol{y}_t|\boldsymbol{y}_{1:t-1})$は、時刻$t$の観測値に対して、最初から1ステップ前の過去の観測値$\boldsymbol{y}_{1:t-1}$をもとに予測したときの実際の観測値$\boldsymbol{y}_t$の確率である。（一期先予測尤度ともいう。）

この$p(\boldsymbol{y}_t|\boldsymbol{y}_{1:t-1})$について、予測分布から考えてみたい。  
時刻$t$の予測分布は$p(\boldsymbol{x}_t | \boldsymbol{y}_{1:t-1})$であり、線形・ガウス状態空間モデルであれば平均ベクトルが$\boldsymbol{x}_{t|t-1}$で、分散共分散行列が$V_{t|t-1}$であるガウス分布に従う。

次に観測モデル$\boldsymbol{y}_t = H_t \boldsymbol{x}_t + \boldsymbol{w}_t$を通すと、
$p(\boldsymbol{y}_t | \boldsymbol{y}_{1:t-1})$は平均ベクトルが$H_t \boldsymbol{x}_{t|t-1}$で、分散共分散行列が$D_{t|t-1}$であるガウス分布に従うとわかる。

![予測分布と一期先予測尤度](prediction_likelihood.png '予測分布と一期先予測尤度')

つまり、$p(\boldsymbol{y}_t | \boldsymbol{y}_{1:t-1})$は以下のように書ける。$1$と$\ell$の違いに注意すること。

$$
\begin{align}
p(\boldsymbol{y}_t|\boldsymbol{y}_{1:t-1}) &= \frac{1}{\sqrt{(2\pi)^\ell \ |D_{t|t-1}|}} \exp \biggl( -\frac{1}{2} (\boldsymbol{y}_t - H_t \boldsymbol{x}_{t|t-1})^{\prime} {D_{t|t-1}}^{-1} (\boldsymbol{y}_t - H_t \boldsymbol{x}_{t|t-1}) \biggr) \\
&= \frac{1}{\sqrt{(2\pi)^\ell \ |D_{t|t-1}|}} \exp \biggl( -\frac{1}{2} {\boldsymbol{e}_t}^{\prime} {D_{t|t-1}}^{-1} {\boldsymbol{e}_t} \biggr)
\end{align}
$$

ところで、もし$p(\boldsymbol{y}_{1:T})$にパラメタベクトル$\boldsymbol{\theta}$（例えばシステムノイズなど）が含まれる場合は、$p(\boldsymbol{y}_{1:T})$は$\boldsymbol{\theta}$の関数とみなせるので、$p(\boldsymbol{y}_{1:T}|\boldsymbol{\theta})$と書いて、これを尤度関数$L(\boldsymbol{\theta})$と呼ぶ。

整理すると以下の通り。

$$
\begin{align}
L(\boldsymbol{\theta}) &= p(\boldsymbol{y}_{1:T}|\boldsymbol{\theta}) \\
&= \prod_{t=1}^{T} p(\boldsymbol{y}_t| \ \boldsymbol{y}_{1:t-1}, \boldsymbol{\theta}) \\
&= \prod_{t=1}^{T} \frac{1}{\sqrt{(2\pi)^\ell \ |D_{t|t-1}|}} \exp \biggl( -\frac{1}{2} {\boldsymbol{e}_t}^{\prime} {D_{t|t-1}}^{-1} {\boldsymbol{e}_t} \biggr)
\end{align}
$$

ただし、尤度関数$L(\boldsymbol{\theta})$は非常に小さい値であるため、ハイスペックな計算機でもアンダフローを起こしてしまう。そこで、尤度関数に対数を導入した対数尤度関数$l(\boldsymbol{\theta})$を求めることで、アンダフローを回避するのが一般的である。

$$
\begin{align}
l(\boldsymbol{\theta}) &= \log L(\boldsymbol{\theta}) \\
&= \log \prod_{t=1}^{T} p(\boldsymbol{y}_t| \ \boldsymbol{y}_{1:t-1}, \boldsymbol{\theta}) \\
&= \sum_{t=1}^{T} \log p(\boldsymbol{y}_t| \ \boldsymbol{y}_{1:t-1}, \boldsymbol{\theta})
\end{align}
$$

ここで、$\log p(\boldsymbol{y}_t| \ \boldsymbol{y}_{1:t-1}, \boldsymbol{\theta})$だけに注目する。

$$
\begin{align}
\log p(\boldsymbol{y}_t| \ \boldsymbol{y}_{1:t-1}, \boldsymbol{\theta})
&= \log \Biggl(\frac{1}{\sqrt{(2\pi)^\ell \ |D_{t|t-1}|}} \exp \biggl( -\frac{1}{2} {\boldsymbol{e}_t}^{\prime} {D_{t|t-1}}^{-1} {\boldsymbol{e}_t} \biggr) \Biggr)\\
&= \log \Biggl( \biggl( (2\pi)^\ell \ |D_{t|t-1}| \biggr) ^{-\frac{1}{2}} \exp \biggl( -\frac{1}{2} {\boldsymbol{e}_t}^{\prime} {D_{t|t-1}}^{-1} {\boldsymbol{e}_t} \biggr) \Biggr)\\
&= -\frac{1}{2} \log \biggl( (2\pi)^\ell \ |D_{t|t-1}| \biggr) + \biggl( -\frac{1}{2} {\boldsymbol{e}_t}^{\prime} {D_{t|t-1}}^{-1} {\boldsymbol{e}_t} \biggr) \\
&= -\frac{\ell}{2} \log 2\pi - \frac{1}{2} \log |D_{t|t-1}| - \frac{1}{2} {\boldsymbol{e}_t}^{\prime} {D_{t|t-1}}^{-1} {\boldsymbol{e}_t}
\end{align}
$$

改めて$l(\boldsymbol{\theta})$に戻ると、以下のように書ける。

$$
\begin{align}
l(\boldsymbol{\theta}) &= \log L(\boldsymbol{\theta}) \\
&= \sum_{t=1}^{T} \log p(\boldsymbol{y}_t| \ \boldsymbol{y}_{1:t-1}, \boldsymbol{\theta}) \\
&= \sum_{t=1}^{T} \biggl( -\frac{\ell}{2} \log 2\pi - \frac{1}{2} \log |D_{t|t-1}| - \frac{1}{2} {\boldsymbol{e}_t}^{\prime} {D_{t|t-1}}^{-1} {\boldsymbol{e}_t} \biggr) \\
&= -\frac{T\ell}{2} \log 2\pi - \frac{1}{2} \sum_{t=1}^{T} \log |D_{t|t-1}| - \frac{1}{2} \sum_{t=1}^{T} {\boldsymbol{e}_t}^{\prime} {D_{t|t-1}}^{-1} {\boldsymbol{e}_t}
\end{align}
$$

**結局、尤度を計算するのは難しいため、この対数尤度関数の値を指標とする。多くの組み合わせの中から、対数尤度関数の値が最大となるパラメタを、最も確からしいとして採用する。なお、この対数尤度関数を単に尤度と呼ぶので注意する。**

このように尤度を比較する場合、$l(\boldsymbol{\theta})$の最終結果にある係数$\frac{1}{2}$は本質的に意味をなさないため、アンダフローを回避する目的で省略することもある。

----------------------------------------------------------------------------

平均
----
平均とは、ある集合におけるもっともよく使われる代表値[^代表値]の1つである。  
平均を求める際は、必ず確率という重みを考慮する必要がある。

[^代表値]: なんでもかんでも平均値を使って議論する人は好きでないです。せめて分散も含めてほしい。

以降では、確率変数がデータ、離散型、連続型の3つの場合に分けて整理する。

### データ
確率変数$X$がデータ値${x_1, x_2, ..., x_n}$であるとき、$X$の平均$m$または$E[X]$は次式で定義する。

$$
m = E[X]= \frac{1}{n} \sum_{k=1}^{n} x_k
$$

<!-- 'E[X] ='とするとなぜか表示されない -->

### 離散型
確率変数$X$が離散型で、確率関数を$P(X=x) = p_k (k=1, 2, ...)$とするとき、$X$の平均$m$または$E[X]$は次式で定義する。

$$
m = E[X]= \sum_{k}^{} x_k p_k
$$

<!-- 'E[X] ='とするとなぜか表示されない -->

上式において、$k$が$k=1, 2, ..., n$で、すべての$k$について$p_k = 1/n$であるとき、確率変数$X$が**データであるときの平均と同じ**になることに注意すること。

### 連続型
確率変数$X$が連続型で、確率密度関数$f(x)$とするとき、$X$の平均$m$または$E[X]$は次式で定義する。

$$
m = E[X]= \int_{-\infty}^{\infty} x f(x) dx
$$

<!-- 'E[X] ='とするとなぜか表示されない -->

分散・標準偏差
--------------
分散とは、ある集合におけるばらつきを示す指標の1つであり、平均を使って定義できる。

確率変数$X$に対し、平均$m$または$E[X]$とするとき、分散$\sigma^{2}$または$V[X]$は次式で定義する。

$$
\sigma^2 = V[X]= E[(X-m)^2]
$$

<!-- 'V[X] ='とするとなぜか表示されない -->

また、$\sigma$を確率変数$X$の標準偏差という。


$$
\sigma = \sqrt{V[X]} = \sqrt{E[(X-m)^2]}
$$

平均と同様に、以降では確率変数がデータ、離散型、連続型の3つの場合に分けて整理する。

### データ
確率変数$X$がデータ値${x_1, x_2, ..., x_n}$であるとき、$X$の分散$\sigma^{2}$または$V[X]$は次式で定義する。

$$
\sigma^2 = V[X]= \frac{1}{n} \sum_{k=1}^{n} (x_k - m)^2
$$

<!-- 'V[X] ='とするとなぜか表示されない -->

### 離散型
確率変数$X$が離散型で、確率関数を$P(X=x) = p_k (k=1, 2, ...)$とするとき、$X$の分散$\sigma^{2}$または$V[X]$は次式で定義する。

$$
\sigma^2 = V[X]= \sum_{k}^{} (x_k - m)^2 p_k
$$

<!-- 'V[X] ='とするとなぜか表示されない -->

### 連続型
確率変数$X$が連続型で、確率密度関数$f(x)$とするとき、$X$の分散$\sigma^{2}$または$V[X]$は次式で定義する。

$$
\sigma^2 = V[X]= \int_{-\infty}^{\infty} (x - m)^2 f(x) dx
$$

<!-- 'V[X] ='とするとなぜか表示されない -->

まとめ
------
上記をまとめると、以下の通り。

|確率変数|平均$m$|分散$\sigma^{2}$|
|:--:|:--:|:--:|
|データ| $\frac{1}{n} \sum_{k=1}^{n} x_k$ | $\frac{1}{n} \sum_{k=1}^{n} (x_k - m)^{2}$ |
|離散型| $\sum_{k}^{} x_k p_k$ | $\sum_{k}^{} (x_k - m)^{2} p_k$ |
|連続型| $\int_{-\infty}^{\infty} x f(x) dx$ | $\int_{-\infty}^{\infty} (x - m)^{2} f(x) dx$ |

<!-- mathjax2hatenatex.pyのあとに'\displaystyle'をつける -->


