//Q3
//-Hàm extended_euclid duoc xay dung truoc do
//  int extended_euclid(int a, int b, int &x, int &y) {
//   if (b == 0) {
//       x = 1;
//        y = 0;
//       return a;
//}
//   int x1, y1;
//    int gcd = extended_euclid(b, a % b, x1, y1);
//    x = y1;
//    y = x1 - (a / b) * y1;
//   return gcd;
//}
//-Hàm main cua chuong trinh tim nghich dao modulo
#include <iostream>
using namespace std;

// Hàm Euclid m? r?ng: tìm x, y sao cho ax + by = gcd(a, b)
int extended_euclid(int a, int b, int &x, int &y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }
    int x1, y1;
    int d = extended_euclid(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return d;
}

int main() {
    int a, b;
    cout << "Nhap a, b: ";
    cin >> a >> b;
    int x, y;
    int gcd = extended_euclid(a, b, x, y);
    cout << "GCD: " << gcd << endl;
    cout << "x = " << x << ", y = " << y << endl;
    // Ki?m tra: ax + by = gcd
    cout << "Check: " << a << "*" << x << " + " << b << "*" << y << " = " << a*x + b*y << endl;
    return 0;
}



