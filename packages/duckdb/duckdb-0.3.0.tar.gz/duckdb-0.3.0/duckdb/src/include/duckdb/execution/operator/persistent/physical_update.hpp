//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/execution/operator/persistent/physical_update.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/execution/physical_sink.hpp"

namespace duckdb {
class DataTable;

//! Physically update data in a table
class PhysicalUpdate : public PhysicalSink {
public:
	PhysicalUpdate(vector<LogicalType> types, TableCatalogEntry &tableref, DataTable &table, vector<column_t> columns,
	               vector<unique_ptr<Expression>> expressions, vector<unique_ptr<Expression>> bound_defaults,
	               idx_t estimated_cardinality)
	    : PhysicalSink(PhysicalOperatorType::UPDATE, move(types), estimated_cardinality), tableref(tableref),
	      table(table), columns(std::move(columns)), expressions(move(expressions)),
	      bound_defaults(move(bound_defaults)) {
	}

	TableCatalogEntry &tableref;
	DataTable &table;
	vector<column_t> columns;
	vector<unique_ptr<Expression>> expressions;
	vector<unique_ptr<Expression>> bound_defaults;
	bool update_is_del_and_insert;

public:
	unique_ptr<GlobalOperatorState> GetGlobalState(ClientContext &context) override;
	unique_ptr<LocalSinkState> GetLocalSinkState(ExecutionContext &context) override;
	void Sink(ExecutionContext &context, GlobalOperatorState &state, LocalSinkState &lstate,
	          DataChunk &input) const override;

	void Combine(ExecutionContext &context, GlobalOperatorState &gstate, LocalSinkState &lstate) override;
	void GetChunkInternal(ExecutionContext &context, DataChunk &chunk, PhysicalOperatorState *state) const override;
};

} // namespace duckdb
