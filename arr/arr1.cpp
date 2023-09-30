#include <iostream>
#include <algorithm>
#include <cstring>

using namespace std;



template <typename T>
class Array
{
public: 
    // Список операций:
    //
    explicit Array(size_t c, const T& t) : m_cnt(c), m_arr(new T[c]) {
        for(size_t i=0;i<c;i++){
            m_arr[i] = t;
        }
    }
    //   конструктор класса, который создает
    //   Array размера size, заполненный значениями
    //   value типа T. Считайте что у типа T есть
    //   конструктор, который можно вызвать без
    //   без параметров, либо он ему не нужен.
    //
    Array(const Array & c){
        m_cnt = c.m_cnt;
        delete[] m_arr;
         for(size_t i=0;i<c;i++){
            m_arr[i] = c[i];
        }
    }
    //   конструктор копирования, который создает
    //   копию параметра. Считайте, что для типа
    //   T определен оператор присваивания.
    //
    Array(const Array && a){
        m_cnt = a.m_cnt;
        swap(a.m_arr.m_arr);
    }
    //
    ~Array(){
        delete[] m_arr;
    }
    //   деструктор, если он вам необходим.
    //
    Array& operator=(const Array & a){
        if(&a != this) {
            m_cnt = a.m_cnt;
            memcpy(m_arr, a.m_arr, m_cnt);
        }
        return *this;
    }
    //   оператор копирующего присваивания.
    //
    Array& operator=(Array && a){
        swap(a.m_cnt, m_cnt);
        swap(a.m_arr, m_arr);
        return *this;
    }
    //   оператор перемещающего присваивания.
    //
    size_t size() const{
        return m_cnt;
    }
    //   возвращает размер массива (количество
    //                              элементов).
    //
    T& operator[](size_t idx){
        return m_arr[idx];
    }
    const T& operator[](size_t idx) const{
        return m_arr[idx];
    }
    //   две версии оператора доступа по индексу.
private:
    size_t m_cnt;
    T* m_arr;
};

template <typename T>
void print(Array<T> &a){
    cout<<a.size()<<" : ";
    for(size_t i =0;i<a.size();i++){
        cout<<a[i];
    }
    cout<<endl;
}

int main()
{
    Array<char> a(10, 'q');
    Array<char> b(7, 'w');
    
    a[3] = 't';
    
    print(a);
    print(b);
    
    a = move(b);
    
    {
        Array<char> c(15, 'e');
        print(c);  
    }
    
    
    print(a);
    print(b);

    return 0;
}