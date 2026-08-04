#include <memory>
#include <iostream>
#include <new>
#include <cstdlib>

static std::size_t bytes_remaining = SIZE_MAX;

void* operator new(std::size_t n) {
    if (n > bytes_remaining) throw std::bad_alloc();
    bytes_remaining -= n;
    return std::malloc(n);
}
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

struct IFunction {
    ~IFunction() { std::cout << "dtor: ptr was cleaned up\n"; }
};

int main() {
    IFunction* ptr = new IFunction();   // uses some budget
    bytes_remaining = 0;                // no room left for the control block
    try {
        std::shared_ptr<IFunction> foo(ptr);  // throws, then deletes ptr
    } catch (std::bad_alloc&) {
        bytes_remaining = SIZE_MAX;
        std::cout << "caught bad_alloc\n";
    }
}
