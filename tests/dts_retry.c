#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include "../src/dts/dts_retry.h"

static int should(int code, long count, uint64_t ns, int stop) {
  return dts_range_retryable(code,count,ns,stop);
}
int main(void) {
  const int temporary[] = {0,206,408,429,500,502,503,504};
  const int permanent[] = {200,201,204,206+1,301,302,400,401,403,404,405,410,412,416,418};
  for (unsigned i=0;i<sizeof temporary/sizeof temporary[0];i++) {
    assert(should(temporary[i],0,0,0));
    assert(should(temporary[i],0,DTS_RANGE_RETRY_FAST_NS,0));
    assert(!should(temporary[i],0,DTS_RANGE_RETRY_FAST_NS+1,0));
    assert(!should(temporary[i],0,UINT64_MAX,0));
    assert(!should(temporary[i],0,10,1));
    assert(!should(temporary[i],128,10,0)); // partial, nonzero data must be kept
  }
  for (unsigned i=0;i<sizeof permanent/sizeof permanent[0];i++)
    assert(!should(permanent[i],0,0,0));
  puts("PASS: DTS retries only fast, empty transient ranges; never permanent/cancelled");
  return 0;
}
