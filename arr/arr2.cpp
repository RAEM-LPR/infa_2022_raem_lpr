#include <iostream>

using namespace std;

struct foo{
    int i;
    foo(int j) : i(j) {}
    foo(const foo & src) : i(src.i) {}
};


template <typename T>
class Array
{
public: 
    // Список операций:
    //
    explicit Array(size_t c, const T& t) : m_cnt(c), m_arr(reinterpret_cast<T*>(new char[c * sizeof(T)])) {
        for(size_t i=0;i<c;i++){
           new (&m_arr[i]) T(t);
        }
    }
    //   конструктор класса, который создает
    //   Array размера size, заполненный значениями
    //   value типа T. Для типа T опредеделен конструктор 
    //   копирования, про конструктор по умолчанию и 
    //   оператор присваивания неизвестно.
    //

    Array(const Array & c){
        m_cnt = c.m_cnt;
        for(size_t i=0;i<c.size;i++){
            new (&m_arr[i]) T(c[i]);
        }
    }
    //   конструктор копирования, который создает
    //   копию параметра. Считайте, что для типа
    //   T не определен оператор присваивания.
    //
    Array(Array && a){
        swap(m_cnt,a.m_cnt);//m_cnt = a.m_cnt;
        swap(a.m_arr.m_arr);
    }
    //   конструктор перемещения
    Array(){
        delete[] m_arr;
    }
    //   деструктор, если он вам необходим.
    //
    Array& operator=(const Array & a){
        if(&a != this) {
            m_cnt = a.m_cnt;
            delete[] m_arr;
            for(size_t i=0;i<a.size;i++){
                new (&m_arr[i]) T(a[i]);
            }
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

std::ostream& operator << (std::ostream &os, const foo &f)
{
    return os << "{" << f.i << "}";
}

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
    Array<foo> a(10, foo(123));
    a[5] = foo(456);
    
    print(a);

    return 0;
}