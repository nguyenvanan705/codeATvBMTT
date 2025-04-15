//Q1
//#include <iostream>
//#include <map>
//#include <cmath>
//#include <string>
//using namespace std;
// calculate entropy
//double calculate_entropy(const string& text) {
//map<char, int> freq;
//for (char c : text) freq[c]++;
//double entropy = 0.0;
//for (auto& pair : freq) {
//double p = (double)pair.second / text.size();
//entropy -= p * log2(p);
//}
//return entropy;
//}
//int main() {
//string input;
//cout << "Enter a string of characters: ";
//getline(cin, input);
//double H = calculate_entropy(input);
//cout << "Entropy: " << H << endl;
//return 0;
//}
//#include <iostream>
//#include <map>
//#include <cmath>
//#include <string>
//using namespace std;
//Import c�c thu vien can thiet: iostream (nh?p xu?t), map (luu t?n su?t k� t?), cmath (h�m to�n h?c), string (x? l� chu?i).

//double calculate_entropy(const string& text) {
    //map<char, int> freq;
    //for (char c : text) freq[c]++;
//H�m calculate_entropy d�ng d? t�nh Entropy cho chu?i d?u v�o text.

//S? d?ng map d? d?m t?n su?t xu?t hi?n c?a t?ng k� t?.

   //double entropy = 0.0;
    //for (auto& pair : freq) {
       // double p = (double)pair.second / text.size();
       // entropy -= p * log2(p);
    //}
   // return entropy;
//}
//T�nh x�c su?t xu?t hi?n p c?a t?ng k� t?.

//cong thuc entrovy o phan 2.1.1
//T?ng h?p l?i d? ra Entropy cu?i c�ng.

//int main() {
    //string input;
    //cout << "Enter a string of characters: ";
    //getline(cin, input);
    //double H = calculate_entropy(input);
    //cout << "Entropy: " << H << endl;
    //return 0;
//}
//H�m main nh?n chu?i t? ngu?i d�ng ? t�nh Entropy ? in k?t qu?.
//Q2
#include <iostream>
#include <cstddef>
#include <map>
#include <cmath>
#include <string>
using namespace std;

// calculate entropy
double calculate_entropy(const string& text) {
    map<char, int> freq;
    for (char c : text) freq[c]++;
}


    double entropy = 0.0;
    int main() {
    string input;
    cout << "Enter a string of characters: ";
    getline(cin, input);

    double H = calculate_entropy(input);
    cout << "Entropy: " << H << endl;

    // �?m b?o do?n for n�y n?m b�n trong h�m main()
    map<char, int> freq;
    for (char c : input) freq[c]++;
    
    int N = freq.size();
    double max_entropy = log2(N);
    double redundancy = max_entropy - H;

    cout << "Max Entropy: " << max_entropy << endl;
    cout << "Redundancy: " << redundancy << endl;

    return 0;
}




