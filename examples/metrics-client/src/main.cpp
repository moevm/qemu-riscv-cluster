#include <prometheus/counter.h>
#include <prometheus/exposer.h>
#include <prometheus/registry.h>

#include <thread>
#include <chrono>

double getMemoryUsed()
{
    uint64_t mem_total = 0, mem_free = 0, buffers = 0, cached = 0;
    FILE *fp = fopen("/proc/meminfo", "r");
    
    static char line[256];
    while (fgets(line, sizeof(line), fp)) {
        if (sscanf(line, "MemTotal: %lu", &mem_total) == 1) continue;
        if (sscanf(line, "MemFree: %lu", &mem_free) == 1) continue;
        if (sscanf(line, "Buffers: %lu", &buffers) == 1) continue;
        if (sscanf(line, "Cached: %lu", &cached) == 1) continue;
    }

    fclose(fp);
    return (double)(mem_total - mem_free - buffers - cached) / (1024.0 * 1024.0);
}

struct {
    uint64_t last_total_user;
    uint64_t last_total_user_low;
    uint64_t last_total_sys;
    uint64_t last_total_idle;
} cpu;

void initCPUInfo()
{
    FILE *file = fopen("/proc/stat", "r");
    fscanf(file, "cpu %lu %lu %lu %lu",
        &cpu.last_total_user, &cpu.last_total_user_low,
        &cpu.last_total_sys, &cpu.last_total_idle
    );
    fclose(file);
}

double getCPUUsage(){
    uint64_t total_user, total_user_low, total_sys, total_idle, total;
    double percent;
    
    FILE *file = fopen("/proc/stat", "r");
    fscanf(file, "cpu %lu %lu %lu %lu",
        &total_user, &total_user_low, &total_sys, &total_idle
    );
    fclose(file);

    if (total_user < cpu.last_total_user || total_user_low < cpu.last_total_user_low ||
        total_sys < cpu.last_total_sys || total_idle < cpu.last_total_idle) {
        // overflow detection
        percent = -1.0;
    }
    else {
        total = (total_user - cpu.last_total_user) + (total_user_low - cpu.last_total_user_low) +
            (total_sys - cpu.last_total_sys);
        
        percent = total;
        total += (total_idle - cpu.last_total_idle);
        percent /= total;
        percent *= 100;
    }

    cpu.last_total_user = total_user;
    cpu.last_total_user_low = total_user_low;
    cpu.last_total_sys = total_sys;
    cpu.last_total_idle = total_idle;

    return percent;
}

int main()
{
    initCPUInfo();
    prometheus::Exposer exposer("0.0.0.0:8080");

    auto registry = std::make_shared<prometheus::Registry>();

    auto &cpu_usage_family = prometheus::BuildGauge()
        .Name("cpu_usage")
        .Help("CPU Usage in percents")
        .Register(*registry);
    
    auto &memory_used_family = prometheus::BuildGauge()
        .Name("memory_used")
        .Help("Memory used in gigabytes")
        .Register(*registry);
    
    auto &request_count_family = prometheus::BuildGauge()
        .Name("request_count")
        .Help("Count of requests (example)")
        .Register(*registry);

    auto &memory_used_gauge = memory_used_family.Add({{ "memory", "all" }});
    auto &cpu_usage_gauge = cpu_usage_family.Add({{ "cpu", "all" }});
    auto &request_count_gauge = request_count_family.Add({{ "requests", "all" }});

    exposer.RegisterCollectable(registry);

    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(1));

        request_count_gauge.Increment(1.0);

        memory_used_gauge.Set(getMemoryUsed());
        cpu_usage_gauge.Set(getCPUUsage());
    }
}
